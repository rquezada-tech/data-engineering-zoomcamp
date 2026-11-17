"""Ingesta del laboratorio 1.

1. Genera un CSV con lecturas INVENTADAS de estaciones meteorológicas (semilla fija = mismos datos para todos).
2. Lo lee en trozos ("chunks") con pandas, como harías con un archivo enorme.
3. Carga cada trozo en la tabla `lecturas` de PostgreSQL.

Uso:  python ingesta.py [--dias 30] [--tabla lecturas]
"""
import argparse
import csv
import os
import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import create_engine, text

ESTACIONES = {
    "EST-01": "Costa",
    "EST-02": "Valle",
    "EST-03": "Cordillera",
    "EST-04": "Desierto",
    "EST-05": "Bosque",
}
BASE_TEMPERATURA = {"Costa": 16, "Valle": 20, "Cordillera": 6, "Desierto": 24, "Bosque": 12}


def generar_csv(ruta: str, dias: int) -> int:
    rng = random.Random(7)
    inicio = datetime(2025, 11, 1)
    filas = 0
    with open(ruta, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["estacion_id", "zona", "medido_en", "temperatura_c", "humedad_pct", "lluvia_mm"])
        for hora in range(dias * 24):
            momento = inicio + timedelta(hours=hora)
            for est, zona in ESTACIONES.items():
                ciclo_diario = 6 * (1 - abs(momento.hour - 15) / 12)  # más calor a las 15:00
                temp = round(BASE_TEMPERATURA[zona] + ciclo_diario + rng.gauss(0, 1.5), 1)
                humedad = max(5, min(100, round(rng.gauss(60, 15))))
                lluvia = round(rng.expovariate(2), 1) if rng.random() < 0.08 else 0.0
                w.writerow([est, zona, momento.isoformat(sep=" "), temp, humedad, lluvia])
                filas += 1
    return filas


def main():
    parser = argparse.ArgumentParser(description="Ingesta de lecturas meteorológicas a PostgreSQL")
    parser.add_argument("--dias", type=int, default=30)
    parser.add_argument("--tabla", default="lecturas")
    parser.add_argument("--tamano-trozo", type=int, default=1000)
    args = parser.parse_args()

    ruta = "/tmp/lecturas.csv"
    total = generar_csv(ruta, args.dias)
    print(f"CSV generado: {total} filas")

    url = "postgresql+psycopg://{u}:{p}@{h}:{port}/{db}".format(
        u=os.environ["PG_USER"], p=os.environ["PG_PASSWORD"], h=os.environ["PG_HOST"],
        port=os.environ.get("PG_PORT", "5432"), db=os.environ["PG_DB"],
    )
    motor = create_engine(url)

    trozos = pd.read_csv(ruta, parse_dates=["medido_en"], chunksize=args.tamano_trozo)
    for n, trozo in enumerate(trozos, start=1):
        # El primer trozo reemplaza la tabla (así puedes repetir la ingesta sin duplicar datos).
        trozo.to_sql(args.tabla, motor, if_exists="replace" if n == 1 else "append", index=False)
        print(f"  trozo {n}: {len(trozo)} filas cargadas")

    with motor.connect() as con:
        cuenta = con.execute(text(f"SELECT COUNT(*) FROM {args.tabla}")).scalar_one()
    print(f"Listo: la tabla '{args.tabla}' tiene {cuenta} filas")


if __name__ == "__main__":
    main()
