"""Borra el dataset y el bucket del laboratorio (solo en LocalCloud) para empezar de cero."""
from comun import BUCKET, DATASET, clientes, ejecutar, titulo


def main():
    bq, gcs = clientes()
    titulo("Limpieza del laboratorio")
    bq.delete_dataset(DATASET, delete_contents=True, not_found_ok=True)
    print(f"Dataset {DATASET} borrado (si existía).")
    bucket = gcs.lookup_bucket(BUCKET)
    if bucket:
        for blob in gcs.list_blobs(BUCKET):
            blob.delete()
        bucket.delete()
        print(f"Bucket gs://{BUCKET} borrado.")
    else:
        print(f"El bucket gs://{BUCKET} no existía.")


if __name__ == "__main__":
    ejecutar(main)
