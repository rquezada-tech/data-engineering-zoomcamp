"""Paso 2: crear un bucket en el Cloud Storage LOCAL y subir los Parquet."""
from comun import BUCKET, CARPETA_DATOS, PREFIJO, clientes, ejecutar, detener, titulo


def main():
    _, gcs = clientes()
    titulo("Paso 2 · Subir los Parquet al bucket local")
    archivos = sorted(CARPETA_DATOS.glob("viajes_*.parquet"))
    if not archivos:
        detener("No hay archivos Parquet en datos/. Primero ejecuta: uv run python lab/01_generar_parquet.py")

    bucket = gcs.lookup_bucket(BUCKET) or gcs.create_bucket(BUCKET)
    print(f"Bucket: gs://{bucket.name}")
    for archivo in archivos:
        blob = bucket.blob(f"{PREFIJO}/{archivo.name}")
        blob.upload_from_filename(str(archivo))
        print(f"  subido gs://{BUCKET}/{blob.name}")

    print("\nContenido del bucket:")
    for blob in gcs.list_blobs(BUCKET, prefix=PREFIJO + "/"):
        print(f"  {blob.name:35s} {blob.size / 1024:6.0f} KB")
    print("\nContinúa con: uv run python lab/03_crear_tabla_externa.py")


if __name__ == "__main__":
    ejecutar(main)
