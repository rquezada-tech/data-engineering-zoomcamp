# Proyecto final local · Disponibilidad de dispositivos (telemetría)

> Parte de la [ruta en español](../../README.md) (adaptación no oficial). La explicación del diseño y cómo usarlo como base para tu propio proyecto está en la [guía del proyecto final](../../docs/es/proyecto-final.md).

**Clasificación:** 🟡 *adaptado a local*: lago y warehouse emulados con LocalCloud. Datos 100 % sintéticos; no usa datos ni credenciales de ninguna cuenta.

## El problema

Una empresa tiene 12 dispositivos (gateways, sensores de temperatura y medidores de energía) en 3 sitios. Cada uno envía un "latido" cada 5 minutos. Operaciones quiere saber **qué dispositivos están cumpliendo el objetivo de 99 % de disponibilidad** y **cómo evoluciona cada sitio día a día**. Además, necesita confiar en que los datos estén bien.

## Arquitectura

```text
 generar ─► datos/raw/fecha=AAAA-MM-DD/eventos.parquet          (tu Mac)
    │
 ingestar ─► gs://telemetria-lago/raw/fecha=.../eventos.parquet  (lago: Cloud Storage local)
             gs://telemetria-lago/seeds/catalogo_dispositivos.csv
    │
 warehouse ─► telemetria.dim_dispositivos        (load job desde CSV)
              telemetria.raw_eventos_externa     (tabla EXTERNA sobre el lago)
              telemetria.stg_eventos             (limpia, PARTITION BY DATE(ts), CLUSTER BY dispositivo_id)
    │
 calidad ─► telemetria.calidad_resultados        (9 controles; si falla uno crítico, el pipeline se detiene)
    │
 metricas ─► telemetria.disponibilidad_diaria    (PARTITION BY dia, CLUSTER BY dispositivo_id)
             telemetria.disponibilidad_dispositivo
    │
 dashboard (Streamlit) ─► 4 indicadores + gráfico por dispositivo + serie diaria por sitio + calidad
```

## Ejecutar

**1. Enciende LocalCloud** desde la raíz del repositorio:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

**2. Corre el pipeline y las pruebas:**

```bash
cd laboratorios/proyecto-final-telemetria
./ejecutar_proyecto.sh
```

Si prefieres ir paso a paso:

```bash
uv sync --group dev
uv run python -m telemetria.pipeline generar
uv run python -m telemetria.pipeline ingestar
uv run python -m telemetria.pipeline warehouse
uv run python -m telemetria.pipeline calidad
uv run python -m telemetria.pipeline metricas
uv run --group dev pytest -q
```

**3. Abre el dashboard:**

```bash
uv run streamlit run dashboard/app.py
```

Se abre en <http://localhost:8501>. Para detenerlo, presiona `Ctrl + C`.

## Resultado esperado

Los datos tienen semilla fija, así que tus números deben coincidir:

| Paso | Resultado |
|---|---|
| generar | 23 624 eventos en 7 archivos; problemas sembrados: 105 duplicados, 21 sin dispositivo, 28 temperaturas imposibles y 14 con fecha futura |
| warehouse | 23 624 filas crudas → 23 484 en staging (140 descartadas = 105 + 21 + 14) |
| calidad | 6 controles críticos OK; alerta `dispositivos_sin_datos_ultimo_dia = 1` (DSP-012) |
| metricas | Disponibilidad global 96,92 %; 4 dispositivos bajo el objetivo: DSP-012 (78,27 %), DSP-009 (91,47 %), DSP-004 (96,23 %) y DSP-007 (98,16 %) |
| pytest | `3 passed` |

Al final del pipeline verás `PIPELINE OK ✅`.

## Cómo comprobarlo

- `uv run --group dev pytest -q`:
  - `tests/test_generador.py` revisa que los datos sean deterministas y que los problemas sembrados existan.
  - `tests/test_pipeline_localcloud.py` corre el pipeline contra LocalCloud y revisa qué dispositivos incumplen. Se salta si el emulador está apagado.
- `uv run python -m telemetria.datos_dashboard` imprime cuántas filas lee el dashboard: 12, 84 y 9.
- Consola de LocalCloud: <http://localhost:5380/>.

## Estructura

| Archivo | Qué contiene |
|---|---|
| `telemetria/config.py` | Fechas, nombres de tablas y umbrales; cámbialos aquí |
| `telemetria/generar.py` | Generador de telemetría sintética con fallas sembradas |
| `telemetria/pasos.py` | Ingesta, warehouse (SQL), controles de calidad y métricas |
| `telemetria/pipeline.py` | Ejecuta los pasos en orden y se detiene ante fallas críticas |
| `telemetria/conexion.py` | Conexión segura: solo LocalCloud, nunca Google Cloud real |
| `telemetria/datos_dashboard.py` | Consultas del dashboard |
| `dashboard/app.py` | Dashboard en Streamlit |
| `seeds/catalogo_dispositivos.csv` | Catálogo de los 12 dispositivos |
| `tests/` | Pruebas con pytest |

## Limitaciones honestas

- **Escala:** son unos 23 mil eventos. El objetivo es aprender el diseño, no medir rendimiento.
- **Costos y bytes:** el emulador no reproduce la facturación ni la poda de particiones al estimar bytes (ver la [guía del módulo 3](../../docs/es/modulo-03-data-warehouse-bigquery.md)).
- **Orquestación:** `telemetria/pipeline.py` ejecuta los pasos en orden, pero no es un orquestador. La [guía del proyecto](../../docs/es/proyecto-final.md#8-mejoras-sugeridas) explica cómo llevarlo a Kestra.

Probado el 2026-11-17 en macOS con Apple Silicon y Python 3.12 arm64: pipeline completo, `pytest` (3 pruebas) y dashboard en Streamlit revisado en el navegador.
