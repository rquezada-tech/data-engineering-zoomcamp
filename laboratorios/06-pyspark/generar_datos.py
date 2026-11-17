"""Paso 1: generar ~50.000 viajes SINTÉTICOS (inventados) en formato Parquet.

Se ejecuta DENTRO del contenedor con spark-submit. La semilla fija (42) hace que
todas las personas obtengan exactamente los mismos datos.
"""
import random
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql import types as T

VIAJES = 50_000
ZONAS = ["Centro", "Norte", "Sur", "Oriente", "Poniente", "Aeropuerto", "Puerto", "Universidad"]
PESOS = [30, 12, 12, 15, 10, 8, 5, 8]
PAGOS = ["tarjeta", "efectivo", "app"]

ESQUEMA = T.StructType(
    [
        T.StructField("viaje_id", T.LongType()),
        T.StructField("inicio", T.TimestampType()),
        T.StructField("fin", T.TimestampType()),
        T.StructField("zona_origen", T.StringType()),
        T.StructField("distancia_km", T.DoubleType()),
        T.StructField("tarifa", T.DoubleType()),
        T.StructField("propina", T.DoubleType()),
        T.StructField("tipo_pago", T.StringType()),
    ]
)


def generar_filas():
    rng = random.Random(42)
    comienzo = datetime(2024, 1, 1)
    segundos = int((datetime(2024, 4, 1) - comienzo).total_seconds())  # enero a marzo de 2024
    for viaje_id in range(1, VIAJES + 1):
        inicio = comienzo + timedelta(seconds=rng.randrange(segundos))
        distancia = round(rng.uniform(0.5, 25.0), 2)
        tarifa = 0.0 if rng.random() < 0.01 else round(1.5 + distancia * 0.9, 2)
        pago = rng.choice(PAGOS)
        propina = 0.0 if pago == "efectivo" else round(tarifa * rng.uniform(0, 0.2), 2)
        yield (
            viaje_id,
            inicio,
            inicio + timedelta(minutes=distancia * rng.uniform(2, 4)),
            rng.choices(ZONAS, weights=PESOS)[0],
            distancia,
            tarifa,
            propina,
            pago,
        )


def main():
    spark = SparkSession.builder.appName("generar-datos").config("spark.sql.session.timeZone", "UTC").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    df = spark.createDataFrame(list(generar_filas()), schema=ESQUEMA)
    df.write.mode("overwrite").parquet("datos/viajes")
    print(f"\nListo: {df.count()} viajes guardados en datos/viajes/ (formato Parquet)\n")
    spark.stop()


if __name__ == "__main__":
    main()
