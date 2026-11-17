"""Los pasos del pipeline: ingesta al lago, carga al warehouse, calidad y métricas.

Cada función recibe los clientes de BigQuery (bq) y Cloud Storage (gcs) ya
conectados a LocalCloud, y devuelve un pequeño resumen para mostrar en pantalla.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from google.cloud import bigquery

from . import config
from .conexion import ErrorLaboratorio


def t(bq, clave: str) -> str:
    """Nombre completo de una tabla del proyecto, con comillas invertidas para SQL."""
    return f"`{bq.project}.{config.DATASET}.{config.TABLAS[clave]}`"


def _sql(bq, consulta: str) -> list:
    return list(bq.query(consulta).result())


# ---------------------------------------------------------------------------
# 1. Ingesta: archivos locales -> lago de datos (Cloud Storage local)
# ---------------------------------------------------------------------------
def ingestar(bq, gcs) -> dict:
    archivos = sorted(config.CARPETA_RAW.glob("fecha=*/eventos.parquet"))
    if not archivos:
        raise ErrorLaboratorio("No hay datos crudos. Ejecuta primero el paso 'generar'.")
    bucket = gcs.lookup_bucket(config.BUCKET) or gcs.create_bucket(config.BUCKET)
    for archivo in archivos:
        ruta = f"{config.PREFIJO_RAW}/{archivo.parent.name}/{archivo.name}"  # raw/fecha=AAAA-MM-DD/eventos.parquet
        bucket.blob(ruta).upload_from_filename(str(archivo))
    bucket.blob(f"{config.PREFIJO_SEEDS}/catalogo_dispositivos.csv").upload_from_filename(str(config.CATALOGO_CSV))
    objetos = list(gcs.list_blobs(config.BUCKET))
    return {"archivos_subidos": len(archivos) + 1, "objetos_en_bucket": len(objetos)}


# ---------------------------------------------------------------------------
# 2. Warehouse: catálogo, tabla externa sobre el lago y tabla de staging limpia
# ---------------------------------------------------------------------------
def cargar_warehouse(bq, gcs) -> dict:
    bq.create_dataset(config.DATASET, exists_ok=True)

    # 2a. Catálogo de dispositivos: "load job" de un CSV del bucket a una tabla interna.
    trabajo = bq.load_table_from_uri(
        f"gs://{config.BUCKET}/{config.PREFIJO_SEEDS}/catalogo_dispositivos.csv",
        f"{bq.project}.{config.DATASET}.{config.TABLAS['catalogo']}",
        job_config=bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=[
                bigquery.SchemaField("dispositivo_id", "STRING"),
                bigquery.SchemaField("tipo", "STRING"),
                bigquery.SchemaField("sitio", "STRING"),
                bigquery.SchemaField("instalado_en", "DATE"),
            ],
        ),
    )
    trabajo.result()

    # 2b. Tabla externa: lee los Parquet directamente desde el lago, sin copiarlos.
    _sql(
        bq,
        f"""
CREATE OR REPLACE EXTERNAL TABLE {t(bq, 'raw')}
OPTIONS (format = 'PARQUET', uris = ['gs://{config.BUCKET}/{config.PREFIJO_RAW}/*'])""",
    )

    # 2c. Staging: tabla interna, limpia, particionada por día y con clustering por dispositivo.
    inicio = config.FECHA_INICIO.isoformat()
    fin = (config.FECHA_INICIO + timedelta(days=config.DIAS)).isoformat()
    _sql(
        bq,
        f"""
CREATE OR REPLACE TABLE {t(bq, 'staging')}
PARTITION BY DATE(ts)
CLUSTER BY dispositivo_id
AS
SELECT
  evento_id,
  dispositivo_id,
  ts,
  estado,
  -- una temperatura imposible no invalida el latido: solo dejamos la medición en NULL
  IF(temperatura_c BETWEEN {config.TEMPERATURA_VALIDA[0]} AND {config.TEMPERATURA_VALIDA[1]}, temperatura_c, NULL) AS temperatura_c,
  bateria_pct,
  senal_dbm,
  firmware
FROM {t(bq, 'raw')}
WHERE dispositivo_id IS NOT NULL                          -- sin dispositivo no sirve
  AND ts >= TIMESTAMP('{inicio}') AND ts < TIMESTAMP('{fin}') -- fuera del periodo = reloj desfasado
QUALIFY ROW_NUMBER() OVER (PARTITION BY evento_id ORDER BY ts) = 1  -- quita duplicados""",
    )
    crudas = _sql(bq, f"SELECT COUNT(*) n FROM {t(bq, 'raw')}")[0].n
    limpias = _sql(bq, f"SELECT COUNT(*) n FROM {t(bq, 'staging')}")[0].n
    return {"filas_crudas": crudas, "filas_staging": limpias, "descartadas": crudas - limpias}


# ---------------------------------------------------------------------------
# 3. Controles de calidad
# ---------------------------------------------------------------------------
def controlar_calidad(bq, gcs) -> dict:
    uno = lambda consulta: _sql(bq, consulta)[0][0]  # noqa: E731
    crudas = uno(f"SELECT COUNT(*) FROM {t(bq, 'raw')}")
    limpias = uno(f"SELECT COUNT(*) FROM {t(bq, 'staging')}")
    pct_desc = round(100 * (crudas - limpias) / crudas, 2) if crudas else 100.0
    lo, hi = config.TEMPERATURA_VALIDA

    # (nombre, severidad, valor observado, umbral legible, ¿pasa?)
    chequeos = [
        ("hay_datos_crudos", "critico", crudas, "> 0", crudas > 0),
        ("pct_filas_descartadas", "critico", pct_desc, f"<= {config.MAX_PCT_DESCARTADAS}", pct_desc <= config.MAX_PCT_DESCARTADAS),
        (
            "staging_sin_duplicados",
            "critico",
            uno(f"SELECT COUNT(*) - COUNT(DISTINCT evento_id) FROM {t(bq, 'staging')}"),
            "= 0",
            None,
        ),
        ("staging_dispositivo_no_nulo", "critico", uno(f"SELECT COUNTIF(dispositivo_id IS NULL) FROM {t(bq, 'staging')}"), "= 0", None),
        (
            "staging_dispositivo_en_catalogo",
            "critico",
            uno(
                f"SELECT COUNT(*) FROM {t(bq, 'staging')} s LEFT JOIN {t(bq, 'catalogo')} c USING (dispositivo_id) "
                "WHERE c.dispositivo_id IS NULL"
            ),
            "= 0",
            None,
        ),
        (
            "estado_valores_permitidos",
            "critico",
            uno(f"SELECT COUNTIF(estado NOT IN ('ok', 'degradado', 'error')) FROM {t(bq, 'staging')}"),
            "= 0",
            None,
        ),
        (
            "raw_duplicados",
            "advertencia",
            uno(f"SELECT COUNT(*) - COUNT(DISTINCT evento_id) FROM {t(bq, 'raw')}"),
            "informativo",
            True,
        ),
        (
            "raw_temperatura_fuera_de_rango",
            "advertencia",
            uno(f"SELECT COUNTIF(temperatura_c NOT BETWEEN {lo} AND {hi}) FROM {t(bq, 'raw')}"),
            "informativo",
            True,
        ),
        (
            "dispositivos_sin_datos_ultimo_dia",
            "advertencia",
            uno(
                f"SELECT COUNT(*) FROM {t(bq, 'catalogo')} c WHERE c.dispositivo_id NOT IN "
                f"(SELECT DISTINCT dispositivo_id FROM {t(bq, 'staging')} "
                f"WHERE DATE(ts) = DATE_ADD(DATE('{config.FECHA_INICIO.isoformat()}'), INTERVAL {config.DIAS - 1} DAY))"
            ),
            "= 0",
            None,
        ),
    ]
    filas = []
    ahora = datetime.now(timezone.utc)
    for nombre, severidad, valor, umbral, pasa in chequeos:
        if pasa is None:  # los chequeos "= 0"
            pasa = valor == 0
        filas.append(
            {
                "ejecutado_en": ahora,
                "chequeo": nombre,
                "severidad": severidad,
                "valor": float(valor),
                "umbral": umbral,
                "resultado": "OK" if pasa else ("FALLA" if severidad == "critico" else "ALERTA"),
            }
        )

    # Guardamos el resultado en una tabla para poder mostrarlo en el dashboard.
    valores = ",\n".join(
        "STRUCT(TIMESTAMP('{ejecutado_en}') AS ejecutado_en, '{chequeo}' AS chequeo, '{severidad}' AS severidad, "
        "{valor} AS valor, '{umbral}' AS umbral, '{resultado}' AS resultado)".format(
            **{**f, "ejecutado_en": f["ejecutado_en"].strftime("%Y-%m-%d %H:%M:%S+00")}
        )
        for f in filas
    )
    _sql(bq, f"CREATE OR REPLACE TABLE {t(bq, 'calidad')} AS SELECT * FROM UNNEST([{valores}])")

    fallas = [f for f in filas if f["resultado"] == "FALLA"]
    return {"chequeos": filas, "fallas_criticas": len(fallas)}


# ---------------------------------------------------------------------------
# 4. Métricas de disponibilidad
# ---------------------------------------------------------------------------
def calcular_metricas(bq, gcs) -> dict:
    # Disponibilidad diaria = intervalos de 5 minutos con al menos un latido "no error" / 288.
    _sql(
        bq,
        f"""
CREATE OR REPLACE TABLE {t(bq, 'diaria')}
PARTITION BY dia
CLUSTER BY dispositivo_id
AS
WITH intervalos AS (
  SELECT
    dispositivo_id,
    DATE(ts) AS dia,
    DIV(UNIX_SECONDS(ts), {config.INTERVALO_MIN * 60}) AS intervalo,
    LOGICAL_OR(estado != 'error') AS operativo,
    AVG(temperatura_c) AS temperatura_c
  FROM {t(bq, 'staging')}
  GROUP BY dispositivo_id, dia, intervalo
),
calendario AS (
  SELECT c.dispositivo_id, c.tipo, c.sitio, dia
  FROM {t(bq, 'catalogo')} c
  CROSS JOIN UNNEST(GENERATE_DATE_ARRAY(DATE('{config.FECHA_INICIO.isoformat()}'),
                                        DATE_ADD(DATE('{config.FECHA_INICIO.isoformat()}'), INTERVAL {config.DIAS - 1} DAY))) AS dia
)
SELECT
  cal.dispositivo_id,
  cal.tipo,
  cal.sitio,
  cal.dia,
  COUNT(i.intervalo) AS intervalos_con_senal,
  COUNTIF(i.operativo) AS intervalos_operativos,
  {config.LATIDOS_POR_DIA} AS intervalos_esperados,
  ROUND(100 * COUNTIF(i.operativo) / {config.LATIDOS_POR_DIA}, 2) AS disponibilidad_pct,
  ({config.LATIDOS_POR_DIA} - COUNT(i.intervalo)) * {config.INTERVALO_MIN} AS minutos_sin_senal,
  ROUND(AVG(i.temperatura_c), 2) AS temperatura_promedio_c
FROM calendario cal
LEFT JOIN intervalos i
  ON i.dispositivo_id = cal.dispositivo_id AND i.dia = cal.dia
GROUP BY cal.dispositivo_id, cal.tipo, cal.sitio, cal.dia""",
    )

    # Resumen por dispositivo para todo el periodo, con el objetivo (SLO) de disponibilidad.
    _sql(
        bq,
        f"""
CREATE OR REPLACE TABLE {t(bq, 'resumen')} AS
SELECT
  dispositivo_id,
  ANY_VALUE(tipo) AS tipo,
  ANY_VALUE(sitio) AS sitio,
  ROUND(100 * SUM(intervalos_operativos) / SUM(intervalos_esperados), 2) AS disponibilidad_pct,
  SUM(minutos_sin_senal) AS minutos_sin_senal,
  COUNTIF(disponibilidad_pct < {config.OBJETIVO_DISPONIBILIDAD}) AS dias_bajo_objetivo,
  ROUND(100 * SUM(intervalos_operativos) / SUM(intervalos_esperados), 2) >= {config.OBJETIVO_DISPONIBILIDAD} AS cumple_objetivo
FROM {t(bq, 'diaria')}
GROUP BY dispositivo_id""",
    )
    filas = _sql(bq, f"SELECT * FROM {t(bq, 'resumen')} ORDER BY disponibilidad_pct, dispositivo_id")
    return {"dispositivos": [dict(f.items()) for f in filas]}
