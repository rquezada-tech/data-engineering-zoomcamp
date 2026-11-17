"""Paso 6: particionamiento, clustering y estimación de bytes (dry run).

IMPORTANTE: los bytes que verás aquí los calcula el EMULADOR. Sirven para practicar
cómo se pide una estimación, pero NO son las cifras que daría BigQuery real.
"""
from google.cloud import bigquery

from comun import TABLA_INTERNA, TABLA_PARTICIONADA, clientes, ejecutar, tabla, titulo


def estimar(bq, sql):
    """Pide a BigQuery que ESTIME cuántos bytes leería la consulta, sin ejecutarla."""
    cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    return bq.query(sql, job_config=cfg).total_bytes_processed


def main():
    bq, _ = clientes()
    titulo("Paso 6 · Particionar y agrupar (clustering)")
    sql = f"""
CREATE OR REPLACE TABLE `{tabla(bq, TABLA_PARTICIONADA)}`
PARTITION BY DATE(inicio)      -- una "cajonera" por día
CLUSTER BY zona_origen         -- dentro de cada cajón, ordenado por zona
AS SELECT * FROM `{tabla(bq, TABLA_INTERNA)}`"""
    print(sql)
    bq.query(sql).result()

    t = bq.get_table(tabla(bq, TABLA_PARTICIONADA))
    print(f"\nParticionada por : {t.time_partitioning.type_} sobre la columna '{t.time_partitioning.field}'")
    print(f"Clustering por   : {t.clustering_fields}")

    particiones = list(
        bq.query(
            f"""
SELECT partition_id, total_rows
FROM `{bq.project}.{t.dataset_id}.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = '{TABLA_PARTICIONADA}'
ORDER BY partition_id"""
        ).result()
    )
    print(f"Particiones      : {len(particiones)} (una por día con datos)")
    for p in particiones[:3]:
        print(f"   {p.partition_id}: {p.total_rows} filas")
    print("   ...")

    titulo("Estimación de bytes (dry run) — cifras del EMULADOR, no de BigQuery real")
    filtro = "WHERE DATE(inicio) BETWEEN '2024-02-01' AND '2024-02-07' AND zona_origen = 'Centro'"
    consultas = {
        "Sin partición, sin filtro": f"SELECT SUM(tarifa) FROM `{tabla(bq, TABLA_INTERNA)}`",
        "Sin partición, 1 semana  ": f"SELECT SUM(tarifa) FROM `{tabla(bq, TABLA_INTERNA)}` {filtro}",
        "Con partición, 1 semana  ": f"SELECT SUM(tarifa) FROM `{tabla(bq, TABLA_PARTICIONADA)}` {filtro}",
    }
    for nombre, consulta in consultas.items():
        print(f"  {nombre}: {estimar(bq, consulta):>8,} bytes (estimación del emulador)")

    # Lo que SÍ podemos medir localmente: qué fracción de particiones necesita la consulta.
    dias = [p for p in particiones if "20240201" <= p.partition_id <= "20240207"]
    filas_semana = sum(p.total_rows for p in dias)
    filas_total = sum(p.total_rows for p in particiones)
    print(
        f"\n  Particiones que la consulta de 1 semana necesita: {len(dias)} de {len(particiones)}"
        f" ({filas_semana} de {filas_total} filas, {100 * filas_semana / filas_total:.1f}%)."
    )
    print("  Ese porcentaje es lo que la poda de particiones ahorra en BigQuery real (aprox.).")

    print(
        """
Cómo leer estos números:
  * En BigQuery REAL, la consulta "con partición, 1 semana" leería solo ~7 de los 91 días,
    así que su estimación bajaría mucho (poda de particiones o "partition pruning").
  * El emulador calcula los bytes de otra forma y NO aplica esa poda en la estimación.
    Por eso aquí practicas CÓMO se pide la estimación y CÓMO se diseña la tabla,
    pero las cifras reales solo se pueden comparar en GCP (ver apéndice opcional).
  * Lo que sí puedes comprobar localmente: cuántas particiones hay y cuántas filas tiene
    cada una (INFORMATION_SCHEMA.PARTITIONS), que es justo lo que BigQuery usa para podar.

Continúa con: uv run python lab/07_comprobar.py"""
    )


if __name__ == "__main__":
    ejecutar(main)
