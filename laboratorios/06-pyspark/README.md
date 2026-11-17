# Laboratorio módulo 6 · PySpark sin instalar Java

> Parte de la [ruta en español](../../README.md) (adaptación no oficial del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) de DataTalks.Club; código original de esta adaptación). Conceptos en la [guía del módulo 6](../../docs/es/modulo-06-pyspark.md).

Spark necesita Java para funcionar. En vez de instalar Java en tu Mac, usamos la imagen oficial
`apache/spark:4.0.1-python3`, que ya trae **Spark 4.0.1 + Java 17 + Python 3.10** y funciona en Apple Silicon (arm64).

## Qué vas a hacer

1. Generar 50.000 viajes inventados (sintéticos) en formato Parquet.
2. Ejecutar un trabajo de Spark que lee, limpia, resume (con DataFrames y con SQL), cruza con una tabla de zonas
   y guarda el resultado en carpetas por mes.

## Paso a paso

Todos los comandos se ejecutan **desde esta carpeta** (`laboratorios/06-pyspark`).

```bash
docker compose up -d --wait
```

La primera vez descarga la imagen (~1 GB). Después, genera los datos:

```bash
docker compose exec spark /opt/spark/bin/spark-submit generar_datos.py
```

Resultado esperado (al final de muchas líneas de registro):

```text
Listo: 50000 viajes guardados en datos/viajes/ (formato Parquet)
```

Ejecuta el trabajo de Spark:

```bash
docker compose exec spark /opt/spark/bin/spark-submit trabajo_spark.py
```

Resultado esperado (resumen):

```text
Versión de Spark: 4.0.1
Filas leídas: 50000
Filas válidas: 49483
+-------+------+---------+
|    mes|viajes| ingresos|
|2024-01| 16782| 217777.6|
|2024-02| 15783|205025.09|
|2024-03| 16918|219104.57|
...
Filas re-leídas desde salida/: 49483
```

Spark imprime muchos mensajes `INFO` y `WARN`; es normal. Si quieres ver solo el resultado, agrega `2>/dev/null` al final del comando.

## Cómo comprobarlo

```bash
ls salida/viajes_por_mes
```

Debes ver `_SUCCESS` (Spark terminó bien) y tres carpetas: `mes=2024-01`, `mes=2024-02`, `mes=2024-03`.
Dentro de cada una hay hasta 4 archivos `part-0000X...parquet`, uno por cada partición creada con `repartition(4)`.

## Mirar la Spark UI (puerto 4040)

La Spark UI es una página web que muestra los *jobs*, *stages* y tareas mientras un trabajo corre.
Solo existe **mientras el trabajo está vivo**. Para tener tiempo de abrirla, pide una pausa de 60 segundos al final:

```bash
docker compose exec -e PAUSA_UI_SEGUNDOS=60 spark /opt/spark/bin/spark-submit trabajo_spark.py
```

Mientras dice "Pausa de 60 s", abre <http://localhost:4040>.

## Detener y limpiar

```bash
docker compose down
```

```bash
rm -rf datos salida
```

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop está cerrado | Ábrelo y espera a que diga "running". |
| `port is already allocated` en 4040 | Otro Spark (u otra app) usa el 4040 | Cierra el otro proceso o cambia `4040:4040` por `4041:4040` en `docker-compose.yml`. |
| `WARN MemoryManager: Total allocation exceeds 95%` | Aviso normal con poca memoria del driver | Se puede ignorar en este laboratorio. |
| `java.lang.OutOfMemoryError` | Docker Desktop tiene poca RAM asignada | En Docker Desktop → Settings → Resources, asigna al menos 4 GB. |
