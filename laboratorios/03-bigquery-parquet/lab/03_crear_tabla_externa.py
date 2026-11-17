"""Paso 3: crear un dataset y una TABLA EXTERNA que lee los Parquet desde el bucket.

Una tabla externa no copia los datos: BigQuery los lee desde Cloud Storage cada vez que consultas.
"""
from comun import BUCKET, DATASET, PREFIJO, TABLA_EXTERNA, clientes, ejecutar, tabla, titulo


def main():
    bq, _ = clientes()
    titulo("Paso 3 · Crear la tabla externa")
    bq.create_dataset(DATASET, exists_ok=True)
    print(f"Dataset listo: {bq.project}.{DATASET}")

    sql = f"""
CREATE OR REPLACE EXTERNAL TABLE `{tabla(bq, TABLA_EXTERNA)}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{BUCKET}/{PREFIJO}/*.parquet']
)"""
    print(sql)
    bq.query(sql).result()

    t = bq.get_table(tabla(bq, TABLA_EXTERNA))
    print(f"\nTipo de tabla: {t.table_type}")
    print("Columnas detectadas desde el Parquet:")
    for campo in t.schema:
        print(f"  {campo.name:14s} {campo.field_type}")
    print("\nContinúa con: uv run python lab/04_consultar_tabla_externa.py")


if __name__ == "__main__":
    ejecutar(main)
