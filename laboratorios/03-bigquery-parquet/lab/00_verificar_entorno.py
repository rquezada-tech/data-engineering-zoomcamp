"""Paso 0: comprobar que LocalCloud está encendido y que los clientes apuntan a tu computador."""
from comun import clientes, configuracion, ejecutar, titulo


def main():
    bq, gcs = clientes()
    cfg = configuracion()
    titulo("Paso 0 · Verificar el entorno")
    print(f"Proyecto local      : {bq.project}")
    print(f"BigQuery (emulado)  : {bq._connection.API_BASE_URL}")
    print(f"Cloud Storage (emul): {gcs._connection.API_BASE_URL}")
    print(f"Gateway LocalCloud  : {cfg['gateway']}")
    # Una consulta mínima para confirmar que BigQuery responde de verdad.
    fila = list(bq.query("SELECT 1 + 1 AS resultado").result())[0]
    print(f"Prueba SELECT 1 + 1 : {fila.resultado}")
    print("\nTodo listo. Continúa con: uv run python lab/01_generar_parquet.py")


if __name__ == "__main__":
    ejecutar(main)
