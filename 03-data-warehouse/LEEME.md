# Mapa en español · 03-data-warehouse

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-03-data-warehouse-bigquery.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo trata sobre el **data warehouse** (almacén de datos): una base de datos pensada para leer y resumir muchísimas filas, no para registrar operaciones una por una. El ejemplo es **BigQuery**, el almacén de Google Cloud. Aprendes a crear tablas a partir de archivos guardados en un bucket, a organizarlas con **particiones** y **clustering** para que las consultas lean menos datos, y cómo funciona BigQuery por dentro. Al final hay un bloque avanzado de **machine learning** (aprendizaje automático) hecho solo con SQL.

## Cómo recorrer esta carpeta

1. Lee primero la [guía en español del módulo](../docs/es/modulo-03-data-warehouse-bigquery.md): explica los conceptos con ejemplos simples.
2. Luego abre las lecciones 01 a 04 en orden. Son la base y casi todo se puede practicar en tu computador.
3. Practica con el [laboratorio 03 · BigQuery + Parquet](../laboratorios/03-bigquery-parquet/README.md), que usa **LocalCloud** (un emulador de Google Cloud que corre en Docker) en lugar de la nube real.
4. Las lecciones 05 y 06 (machine learning) son opcionales y necesitan una cuenta de Google Cloud. Léelas para entender la idea y revisa el [apéndice de GCP](../docs/es/apendice-gcp.md) si algún día quieres ejecutarlas.
5. Para la tarea, usa la de la cohorte 2026: [`../cohorts/2026/03-data-warehouse/homework.md`](../cohorts/2026/03-data-warehouse/homework.md). La guía en español clasifica cada pregunta.

## Lecciones

Leyenda: 🟢 local sin cambios · 🟡 adaptado a local · 🔴 requiere GCP o cuenta externa.

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [Data Warehouse and BigQuery](01-data-warehouse-and-bigquery.md) | Compara bases de datos transaccionales y analíticas, presenta BigQuery y sus modelos de cobro, y hace un primer recorrido: datos públicos, tablas externas sobre archivos en un bucket, y las primeras tablas particionadas y con clustering. | 🟡 LocalCloud (laboratorio 03, pasos 02 a 06). Las cifras de bytes y costos reales: 🔴 |
| 02 | [Partitioning vs Clustering](02-partitioning-vs-clustering.md) | Profundiza en las opciones para particionar una tabla, en cómo el clustering ordena las filas y en los criterios para elegir uno, otro o ambos. | 🟡 LocalCloud: el `PARTITION BY` y el `CLUSTER BY` funcionan igual. El ahorro medido en bytes: 🔴 |
| 03 | [BigQuery Best Practices](03-bigquery-best-practices.md) | Lista corta de hábitos para gastar menos y consultar más rápido, como pedir solo las columnas que necesitas y filtrar por la columna de partición. | 🟢 Conceptual. Comprobar el ahorro en dinero: 🔴 |
| 04 | [Internals of BigQuery](04-internals-of-bigquery.md) | Explica cómo está construido BigQuery por dentro: almacenamiento separado del cómputo, la red que los une, el formato por columnas y cómo una consulta se reparte en un árbol de servidores. | 🟢 Conceptual, no requiere ejecutar nada |
| 05 | [Machine Learning in BigQuery](05-machine-learning-in-bigquery.md) | Entrena con SQL un modelo que predice la propina de un viaje, lo evalúa, explica sus predicciones y prueba distintos ajustes (BigQuery ML). | 🔴 Requiere GCP (BigQuery ML) |
| 06 | [Deploying a Machine Learning Model](06-deploying-a-machine-learning-model.md) | Exporta el modelo de la lección anterior a Cloud Storage, lo descarga y lo publica en un contenedor Docker para pedirle predicciones por HTTP. | 🔴 Requiere GCP (el modelo sale de BigQuery ML) |

## Código y otros archivos

| Archivo o carpeta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice del módulo con la lista de lecciones y enlaces a apuntes de la comunidad. | Para orientarte; la sección de tarea está vacía en esta versión. |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo (título, resumen y orden de las lecciones) que usa la plataforma del curso. | Casi nunca; no es material de estudio. |
| [`big_query.sql`](big_query.sql) | Todas las consultas SQL de las lecciones 01 y 02: tabla externa, tablas particionadas y con clustering, y comparaciones. | Mientras ves las lecciones 01 y 02. En LocalCloud tendrás que cambiar el nombre del proyecto y del bucket. |
| [`big_query_hw.sql`](big_query_hw.sql) | Consultas de una tarea de un año anterior con datos FHV (vehículos de alquiler con conductor). | Solo como ejemplo extra; no corresponde a la tarea 2026. |
| [`big_query_ml.sql`](big_query_ml.sql) | Las consultas de BigQuery ML de la lección 05. | Solo si tienes cuenta de GCP. 🔴 |
| [`load_yellow_taxi_data.py`](load_yellow_taxi_data.py) | Script de Python que descarga los Parquet de taxis amarillos de enero a junio de 2024 y los sube a un bucket de Cloud Storage. | Para preparar los datos de la tarea 2026 en GCP real. Se puede adaptar a LocalCloud (no probado en esta ruta). |
| [`DLT_upload_to_GCP.ipynb`](DLT_upload_to_GCP.ipynb) | Notebook (pensado para Google Colab) que usa `dlt` para cargar los mismos Parquet a un bucket o, para pruebas, a DuckDB. | Alternativa al script anterior. La opción DuckDB es 🟢; la de GCS es 🔴. |
| [`extras/`](extras/README.md) | Scripts `web_to_gcs.py` y `web_to_gcs_with_progress_bar.py` que bajan los CSV de taxis y los suben a Cloud Storage como Parquet, sin orquestador. Incluye `pyproject.toml` y un `.env-example`. | Solo si quieres cargar datos a un bucket real sin usar Kestra. 🔴 |
| `images/` | Capturas de pantalla, diagramas (con sus fuentes `.json`) y miniaturas de los videos. | No necesitas abrirla: las lecciones ya muestran las imágenes. |

> Los archivos `load_yellow_taxi_data.py` y `DLT_upload_to_GCP.ipynb` son idénticos a los que están en `cohorts/2026/03-data-warehouse/`.

## Palabras en inglés que vas a encontrar

| Término | Significado sencillo |
|---|---|
| Data warehouse | Almacén de datos: base de datos optimizada para análisis sobre grandes volúmenes. |
| OLTP / OLAP | Bases para operaciones del día a día (OLTP) frente a bases para análisis (OLAP). |
| Data mart | Porción del almacén dedicada a un tema o área, como ventas o inventario. |
| Bucket | "Carpeta raíz" donde Cloud Storage guarda archivos. |
| External table | Tabla externa: BigQuery solo guarda la ruta a los archivos y los lee al consultar. |
| Partitioning | Particionamiento: dividir una tabla en trozos, normalmente por fecha, para leer solo los necesarios. |
| Clustering | Ordenar las filas por una o más columnas para saltarse bloques al filtrar. |
| Columnar storage | Almacenamiento por columnas: cada columna se guarda aparte. |
| Slot | Unidad de capacidad de cómputo que BigQuery asigna a una consulta. |
| On-demand pricing | Cobro según los bytes que lee cada consulta. |
| Dry run | Estimar cuánto leería una consulta sin ejecutarla. |
| Feature / label | En machine learning: las columnas de entrada (features) y el valor que se quiere predecir (label). |
| Serving | Publicar un modelo para que otros programas le pidan predicciones. |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la cohorte **2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de esta carpeta, preparada para 2027. En 2026 el `README.md` era solo una lista de videos y diapositivas; ahora cada video tiene su propia lección escrita (`01-…md` a `06-…md`) con diagramas nuevos, y el antiguo `extract_model.md` quedó absorbido en la lección 06. También se agregaron aquí `load_yellow_taxi_data.py`, `DLT_upload_to_GCP.ipynb` y `module.yaml`, y la sección de tarea quedó vacía. Los conceptos y los videos son los mismos, pero **los enlaces de las guías en español apuntan a la versión 2026**, así que lo que veas allá puede no coincidir línea por línea con esta carpeta.
