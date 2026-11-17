"""Paso 5: MATERIALIZAR el resultado en una tabla interna (nativa) de BigQuery.

"Materializar" = guardar una copia de los datos dentro de BigQuery. Desde ahora
las consultas ya no dependen de los archivos del bucket.
"""
from comun import TABLA_EXTERNA, TABLA_INTERNA, clientes, ejecutar, tabla, titulo


def main():
    bq, _ = clientes()
    titulo("Paso 5 · Materializar en una tabla interna")
    sql = f"""
CREATE OR REPLACE TABLE `{tabla(bq, TABLA_INTERNA)}` AS
SELECT
  viaje_id,
  inicio,
  fin,
  zona_origen,
  distancia_km,
  tarifa,
  propina,
  tipo_pago,
  TIMESTAMP_DIFF(fin, inicio, MINUTE) AS duracion_min
FROM `{tabla(bq, TABLA_EXTERNA)}`
WHERE tarifa > 0  -- limpiamos: dejamos fuera los viajes con tarifa 0"""
    print(sql)
    bq.query(sql).result()
    t = bq.get_table(tabla(bq, TABLA_INTERNA))
    print(f"\nTabla creada: {t.full_table_id}")
    print(f"Tipo        : {t.table_type}  (BASE TABLE / TABLE = tabla interna)")
    print(f"Filas       : {t.num_rows}")
    print("\nContinúa con: uv run python lab/06_particion_y_clustering.py")


if __name__ == "__main__":
    ejecutar(main)
