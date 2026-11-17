# Mapa en español · 06-batch

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-06-pyspark.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo trata del **procesamiento por lotes** (*batch*): tomar un montón de datos acumulados, por ejemplo todos los viajes de un día, y procesarlos de una sola vez. La herramienta central es **Apache Spark**, un motor que reparte el trabajo entre muchos núcleos o máquinas, y se usa desde Python con **PySpark**. Vas a leer datos de taxis de Nueva York, transformarlos con DataFrames y con SQL, y mirar por dentro cómo Spark agrupa y une tablas. La parte final muestra cómo llevar ese mismo trabajo a Google Cloud (Cloud Storage, Dataproc y BigQuery).

## Cómo recorrer esta carpeta

1. **Empieza en español:** lee la [guía del módulo 6](../docs/es/modulo-06-pyspark.md) y haz el [laboratorio de PySpark](../laboratorios/06-pyspark/README.md). Corre Spark dentro de Docker, así que no tienes que instalar Java.
2. **Luego, las lecciones 01 a 10**, en orden. Son la columna vertebral del módulo: qué es Spark, DataFrames, SQL y cómo funciona por dentro. Cada lección tiene su video y, al final, una sección `Materials` con el cuaderno de `code/` que la acompaña.
3. **Las lecciones 03, 06, 11 y 12 son opcionales** según el propio curso. Puedes saltarte la 03 si usas el laboratorio, y la 06 si no vas a reproducir los cuadernos con los datos reales.
4. **Las lecciones 13 a 16 (Spark en la nube) requieren una cuenta de Google Cloud.** Léelas para entender la idea y revisa el [apéndice de GCP](../docs/es/apendice-gcp.md) si algún día quieres hacerlas.
5. **Para la tarea oficial 2026**, sigue la sección 8 de la guía, que indica qué preguntas se pueden responder en local.

## Lecciones

Entre paréntesis va el número que tenía cada video en la versión 2026 (por ejemplo, 6.6.1). Lo vas a ver en las guías en español y en la [clasificación de ejercicios](../docs/es/clasificacion-ejercicios.md).

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 (6.1.1) | [Introduction to Batch Processing](01-introduction-to-batch-processing.md) | Explica la diferencia entre procesar por lotes y procesar en flujo continuo (*streaming*), cada cuánto suelen correr los trabajos batch y qué ventajas y desventajas tienen. Es una lección de conceptos. | 🟢 Local sin cambios (solo lectura; resumido en la guía, sección 1) |
| 02 (6.1.2) | [Introduction to Spark](02-introduction-to-spark.md) | Presenta Spark como motor de procesamiento distribuido, los lenguajes con que se usa y cuándo conviene en vez de escribir solo SQL. | 🟢 Local sin cambios (solo lectura) |
| 03 (6.2.1) | [Installing Spark](03-installing-spark.md) | Recorre la instalación de Java y Spark en Linux y enlaza las guías escritas de `setup/` para Windows, Linux y macOS. Opcional. | 🟡 Adaptado a local: el laboratorio usa la imagen Docker `apache/spark:4.0.1-python3` en vez de instalar Java |
| 04 (6.3.1) | [First Look at Spark/PySpark](04-first-look-at-spark.md) | Primer contacto práctico: crear una `SparkSession`, leer un CSV grande, entender las particiones, guardar en Parquet y mirar la Spark UI. | 🟢 Local sin cambios (también en el laboratorio) |
| 05 (6.3.2) | [Spark DataFrames](05-spark-dataframes.md) | Profundiza en los DataFrames de Spark: en qué se parecen a los de pandas, la diferencia entre transformaciones y acciones, y cómo crear funciones propias. | 🟢 Local sin cambios |
| 06 (6.3.3) | [Preparing Yellow and Green Taxi Data](06-preparing-taxi-data.md) | Descarga los datos de taxis amarillos y verdes de 2020 y 2021, les define un esquema explícito y los convierte a Parquet para el resto del módulo. Opcional. | 🟢 Local sin cambios (necesita internet y espacio en disco) |
| 07 (6.3.4) | [SQL with Spark](07-sql-with-spark.md) | Junta los taxis verdes y amarillos en una sola tabla y calcula un reporte de ingresos escribiendo SQL dentro de Spark. | 🟢 Local sin cambios (también en el laboratorio) |
| 08 (6.4.1) | [Anatomy of a Spark Cluster](08-anatomy-of-a-spark-cluster.md) | Describe las piezas de un clúster real (*driver*, *master* y *executors*) y por qué hoy se guardan los datos en un bucket en la nube en vez de HDFS. | 🟢 Local sin cambios (solo lectura; resumido en la guía, sección 2) |
| 09 (6.4.2) | [GroupBy in Spark](09-groupby-in-spark.md) | Sigue paso a paso, en la Spark UI, cómo se ejecuta un `GROUP BY` y dónde ocurre el *shuffle*. | 🟢 Local sin cambios |
| 10 (6.4.3) | [Joins in Spark](10-joins-in-spark.md) | Compara cómo Spark une dos tablas grandes y cómo une una tabla grande con una pequeña (*broadcast*). | 🟢 Local sin cambios |
| 11 (6.5.1) | [Operations on Spark RDDs](11-operations-on-spark-rdds.md) | Baja un nivel, a los RDD, y rehace el reporte de ingresos con operaciones básicas para ver cómo funcionaba Spark antes de los DataFrames. Opcional. | 🟢 Local sin cambios |
| 12 (6.5.2) | [Spark RDD mapPartition](12-spark-rdd-mappartition.md) | Muestra cómo procesar los datos partición por partición, con el ejemplo de aplicar un modelo de predicción a trozos del dataset. Opcional. | 🟢 Local sin cambios |
| 13 (6.6.1) | [Connecting to Google Cloud Storage](13-connecting-to-google-cloud-storage.md) | Sube los Parquet a un bucket de Google Cloud Storage y configura Spark con un conector para leerlos desde ahí. | 🔴 Requiere GCP (el conector no se probó contra LocalCloud) |
| 14 (6.6.2) | [Creating a Local Spark Cluster](14-creating-a-local-spark-cluster.md) | Convierte el cuaderno en un script, levanta un clúster de Spark independiente en tu propia máquina y le envía el trabajo con `spark-submit`. | 🟢 Local (necesitas Spark instalado; esta ruta no probó el clúster independiente) |
| 15 (6.6.3) | [Setting up a Dataproc Cluster](15-setting-up-a-dataproc-cluster.md) | Crea un clúster administrado en Dataproc, el servicio de Spark de Google Cloud, y ejecuta ahí el mismo script. | 🔴 Requiere GCP |
| 16 (6.6.4) | [Connecting Spark to BigQuery](16-connecting-spark-to-bigquery.md) | Cambia la salida del script para que el resultado se guarde directamente como tabla en BigQuery. | 🔴 Requiere GCP |

## Código y otros archivos

| Ruta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice oficial del módulo, con las 16 lecciones y notas de la comunidad | Para ver el orden oficial y buscar apuntes de otros estudiantes |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo: título, resumen y lista de lecciones | No la necesitas como estudiante; la usa la plataforma del curso |
| [`setup/`](setup/) | Guías de instalación de Spark 4 para [Windows](setup/windows.md), [Linux](setup/linux.md) y [macOS](setup/macos.md) | Si quieres instalar Java y PySpark en tu máquina, sin Docker |
| [`setup/hadoop-yarn.md`](setup/hadoop-yarn.md) | Guía para instalar Hadoop y YARN, un gestor de recursos de clúster, en modo de prueba | Casi nunca: la lección 03 la menciona para un material de Spark con Docker que no forma parte de estas lecciones |
| [`setup/config/`](setup/config/) | Archivos de configuración de ejemplo (`core-site.xml`, `spark-defaults.conf`, `spark.dockerfile`) para Spark sobre YARN conectado a GCS | Solo si exploras YARN o las lecciones de la nube |
| [`code/03_test.ipynb`](code/03_test.ipynb) | Cuaderno de prueba: inicia Spark, lee la tabla de zonas y la guarda en Parquet | Lección 04, para comprobar que tu instalación funciona |
| [`code/04_pyspark.ipynb`](code/04_pyspark.ipynb) | Esquemas, reparticionado, escritura en Parquet, acciones y transformaciones | Lecciones 04 y 05 |
| [`code/download_data.sh`](code/download_data.sh) y [`code/05_taxi_schema.ipynb`](code/05_taxi_schema.ipynb) | Script que descarga los CSV de taxis por mes, y cuaderno que les pone esquema y los pasa a Parquet | Lección 06, y antes de las lecciones 07 a 12 si usas los datos reales |
| [`code/06_spark_sql.ipynb`](code/06_spark_sql.ipynb) | Cuaderno con la unión de taxis verdes y amarillos y el reporte de ingresos en SQL | Lección 07 |
| [`code/06_spark_sql.py`](code/06_spark_sql.py) | El mismo reporte como script con parámetros de entrada y salida | Lecciones 14 y 15 |
| [`code/06_spark_sql_big_query.py`](code/06_spark_sql_big_query.py) | Variante del script que escribe el resultado en BigQuery | Lección 16 (🔴) |
| [`code/07_groupby_join.ipynb`](code/07_groupby_join.ipynb) | Agrupaciones y uniones sobre los datos de taxis | Lecciones 09 y 10 |
| [`code/08_rdds.ipynb`](code/08_rdds.ipynb) | Operaciones con RDD y procesamiento por particiones | Lecciones 11 y 12 |
| [`code/09_spark_gcs.ipynb`](code/09_spark_gcs.ipynb) | Configuración de Spark para leer desde un bucket de GCS | Lección 13 (🔴) |
| [`code/homework.ipynb`](code/homework.ipynb) | Cuaderno de una tarea de una cohorte anterior (viajes FHVHV de febrero de 2021) | Solo como referencia; no es la tarea 2026 |
| `images/` | Capturas de pantalla y diagramas de las lecciones (`.png`, `.jpg`, `.svg` y su descripción en `.json`) | No hace falta abrirla: las lecciones ya muestran las imágenes |

## Palabras en inglés que vas a encontrar

| Término | Qué significa |
|---|---|
| *batch processing* | Procesamiento por lotes: procesar de una vez datos acumulados durante un periodo |
| *engine* | Motor: el programa que hace el trabajo pesado de leer, calcular y escribir |
| *cluster* | Grupo de computadores que trabajan juntos como si fueran uno |
| *driver* | El programa que escribes y que planifica el trabajo; no procesa los datos |
| *executor* | Proceso que hace el trabajo real sobre una parte de los datos |
| *partition* | Partición: cada pedazo en que Spark divide los datos para procesarlos en paralelo |
| *schema* | Esquema: la lista de columnas y el tipo de dato de cada una |
| *action* / *transformation* | Acción (ejecuta el plan, como `show`) / transformación (solo agrega un paso al plan, como `filter`) |
| *lazy evaluation* | Evaluación perezosa: Spark no ejecuta nada hasta que pides una acción |
| *shuffle* / *reshuffling* | Mover datos entre executors para agrupar o unir; es la operación más costosa |
| *broadcast join* | Unión en la que se envía una copia de la tabla pequeña a cada executor |
| *RDD* (*Resilient Distributed Dataset*) | La estructura más básica de Spark: una colección distribuida de objetos sin esquema |
| *temp table* / *temp view* | Tabla temporal: un nombre para consultar un DataFrame con SQL |
| *bucket* | "Bodega" de archivos en Google Cloud Storage |
| *spark-submit* | Comando que envía un script de Python a un clúster de Spark para que lo ejecute |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la **cohorte 2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de la carpeta, preparada para 2027. En 2026, el `README.md` era una lista de videos numerados de 6.1.1 a 6.6.4 con un enlace a la tarea, y las instrucciones de la nube estaban en `code/cloud.md`. Ahora, cada video tiene su propia lección escrita (`01-…16-*.md`) con capturas, se agregó `module.yaml`, y `code/cloud.md` desapareció porque su contenido pasó a las lecciones 13 a 16. Los videos, los cuadernos de `code/` y las guías de `setup/` son los mismos. La sección de tarea del `README.md` quedó vacía: la tarea 2026 está en [`../cohorts/2026/06-batch/homework.md`](../cohorts/2026/06-batch/homework.md), y la de 2027 es un borrador. Recuerda que los enlaces de las guías en español apuntan a la versión 2026.
