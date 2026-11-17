"""Paso 2: un trabajo batch con PySpark.

Lee los Parquet, los limpia, los resume con DataFrames y con SQL, los cruza con
una tabla de zonas y guarda el resultado particionado por mes.
"""
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def titulo(texto):
    print("\n" + texto + "\n" + "-" * len(texto))


def main():
    spark = (
        SparkSession.builder.appName("trabajo-viajes")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "8")  # pocos datos -> pocas particiones de shuffle
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    print(f"Versión de Spark: {spark.version}")
    print("Spark UI (mientras corre): http://localhost:4040")

    # 1) Leer ----------------------------------------------------------------
    viajes = spark.read.parquet("datos/viajes")
    titulo("1) Esquema leído desde el Parquet")
    viajes.printSchema()
    print(f"Filas leídas: {viajes.count()}")

    # 2) Transformar con DataFrames -----------------------------------------
    limpios = (
        viajes.filter(F.col("tarifa") > 0)  # fuera viajes con tarifa 0
        .withColumn("duracion_min", F.round((F.unix_timestamp("fin") - F.unix_timestamp("inicio")) / 60, 1))
        .withColumn("mes", F.date_format("inicio", "yyyy-MM"))
    )
    titulo("2) Viajes válidos (tarifa > 0), primeras filas")
    limpios.select("viaje_id", "inicio", "zona_origen", "distancia_km", "tarifa", "duracion_min", "mes").show(5)
    print(f"Filas válidas: {limpios.count()}")

    # 3) Spark SQL -------------------------------------------------------------
    limpios.createOrReplaceTempView("viajes")
    titulo("3) Spark SQL: viajes e ingresos por mes")
    spark.sql(
        """
        SELECT mes, COUNT(*) AS viajes, ROUND(SUM(tarifa), 2) AS ingresos
        FROM viajes
        GROUP BY mes
        ORDER BY mes
        """
    ).show()

    # 4) groupBy + join con una tabla pequeña de zonas -------------------------
    zonas = spark.createDataFrame(
        [
            ("Centro", "urbana"), ("Norte", "residencial"), ("Sur", "residencial"),
            ("Oriente", "residencial"), ("Poniente", "residencial"), ("Aeropuerto", "transporte"),
            ("Puerto", "transporte"), ("Universidad", "urbana"),
        ],
        ["zona_origen", "tipo_zona"],
    )
    titulo("4) groupBy + join: viajes por tipo de zona")
    por_tipo = (
        limpios.join(F.broadcast(zonas), on="zona_origen", how="left")
        .groupBy("tipo_zona")
        .agg(F.count("*").alias("viajes"), F.round(F.avg("tarifa"), 2).alias("tarifa_promedio"))
        .orderBy(F.desc("viajes"))
    )
    por_tipo.show()

    # 5) Repartir y escribir particionado por mes ------------------------------
    titulo("5) Escribir resultado en salida/ (4 particiones, carpetas por mes)")
    limpios.repartition(4).write.mode("overwrite").partitionBy("mes").parquet("salida/viajes_por_mes")
    releido = spark.read.parquet("salida/viajes_por_mes")
    print(f"Filas re-leídas desde salida/: {releido.count()}")
    releido.groupBy("mes").count().orderBy("mes").show()

    # Pausa opcional para mirar la Spark UI antes de que el trabajo termine.
    import os
    espera = int(os.environ.get("PAUSA_UI_SEGUNDOS", "0"))
    if espera:
        print(f"Pausa de {espera} s: abre http://localhost:4040 en tu navegador.")
        time.sleep(espera)
    spark.stop()


if __name__ == "__main__":
    main()
