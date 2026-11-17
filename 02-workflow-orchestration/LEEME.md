# Mapa en español · 02-workflow-orchestration

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-02-kestra.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo trata de la **orquestación**: lograr que varios pasos de datos se ejecuten solos, en el orden correcto, a la hora indicada y dejando registro de lo que pasó. La herramienta del curso es **Kestra**, que se instala con Docker Compose y en la que cada proceso se describe en un archivo YAML llamado *flow* (flujo). Primero cargas los viajes de taxis de Nueva York en el PostgreSQL local del módulo 1, aprendes a programar ejecuciones y a rellenar fechas pasadas (*backfill*). Luego se repite lo mismo en Google Cloud con el enfoque ELT y, al final, hay una parte opcional sobre cómo usar inteligencia artificial para escribir flujos.

## Cómo recorrer esta carpeta

1. Lee la [guía en español del módulo 2](../docs/es/modulo-02-kestra.md): explica flujos, tareas, *triggers*, *backfill*, idempotencia y la diferencia entre ETL y ELT.
2. Haz el [laboratorio 02 · Kestra](../laboratorios/02-kestra/README.md), con flujos propios comentados en español y un resultado esperado exacto.
3. Vuelve aquí y sigue las lecciones `01` a `08`: todas funcionan en tu Mac con el [`docker-compose.yml`](docker-compose.yml) de esta carpeta. Cada lección enlaza el flujo de [`flows/`](flows/) que le corresponde.
4. La lección `09` es conceptual. Las lecciones `10` a `12` y `17` necesitan Google Cloud: léelas para entender la idea y practica el enfoque ELT en local con el [laboratorio 03](../laboratorios/03-bigquery-parquet/README.md).
5. Las lecciones `13` a `16` (IA) son opcionales y necesitan cuentas externas.

## Lecciones

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [`01-what-is-workflow-orchestration.md`](01-what-is-workflow-orchestration.md) | Explica con una analogía musical qué hace un orquestador y por qué es útil cuando hay varios pasos y herramientas que coordinar. | 🟢 Solo lectura |
| 02 | [`02-what-is-kestra.md`](02-what-is-kestra.md) | Presenta Kestra y sus puntos fuertes: flujos en YAML, muchos *plugins*, cualquier lenguaje y disparadores por horario o por eventos. | 🟢 Solo lectura |
| 03 | [`03-installing-kestra.md`](03-installing-kestra.md) | Enciende Kestra con `docker compose up -d` y muestra dos formas de cargar los flujos: pegarlos en el editor web o subirlos con `curl` a la API. | 🟢 Local sin cambios · [lab 02](../laboratorios/02-kestra/README.md) |
| 04 | [`04-kestra-concepts.md`](04-kestra-concepts.md) | Repasa los conceptos básicos (flujo, tarea, *inputs*, *outputs*, *triggers*, ejecución, variables, valores por defecto y concurrencia) usando `01_hello_world.yaml` como ejemplo. | 🟢 Local sin cambios · [lab 02](../laboratorios/02-kestra/README.md) |
| 05 | [`05-orchestrate-python-code.md`](05-orchestrate-python-code.md) | Muestra cómo Kestra ejecuta un script de Python dentro de un contenedor y recupera su resultado (`02_python.yaml`). | 🟢 Local sin cambios (necesita internet) |
| 06 | [`06-getting-started-pipeline.md`](06-getting-started-pipeline.md) | Un primer *pipeline* completo de ejemplo: descarga datos de una API, los transforma con Python y los consulta con DuckDB (`03_getting_started_data_pipeline.yaml`). | 🟢 Local sin cambios (necesita internet) |
| 07 | [`07-load-taxi-data-to-postgres.md`](07-load-taxi-data-to-postgres.md) | El flujo principal en local: elige tipo de taxi, año y mes, descarga el CSV y lo carga y fusiona en Postgres (`04_postgres_taxi.yaml`). | 🟢 Local sin cambios · [lab 02](../laboratorios/02-kestra/README.md) |
| 08 | [`08-scheduling-and-backfills.md`](08-scheduling-and-backfills.md) | Agrega un horario diario al flujo anterior y enseña a rellenar meses pasados de taxis verdes (`05_postgres_taxi_scheduled.yaml`). | 🟢 Local sin cambios · [lab 02](../laboratorios/02-kestra/README.md) |
| 09 | [`09-etl-vs-elt.md`](09-etl-vs-elt.md) | Compara transformar los datos antes de cargarlos (ETL) con cargarlos crudos y transformarlos dentro del almacén de datos (ELT). | 🟢 Solo lectura · el ELT se practica en 🟡 [lab 03](../laboratorios/03-bigquery-parquet/README.md) con LocalCloud |
| 10 | [`10-setup-google-cloud-platform.md`](10-setup-google-cloud-platform.md) | Guarda en el almacén de claves de Kestra los datos de tu proyecto de GCP y crea el *bucket* y el *dataset* (`06_gcp_kv.yaml`, `07_gcp_setup.yaml`). | 🔴 Requiere GCP · [apéndice](../docs/es/apendice-gcp.md) (sección 5) |
| 11 | [`11-load-taxi-data-to-bigquery.md`](11-load-taxi-data-to-bigquery.md) | Versión en la nube del flujo de la lección 07: sube el CSV a Cloud Storage, crea una tabla externa en BigQuery y fusiona los datos (`08_gcp_taxi.yaml`). | 🔴 Requiere GCP · alternativa 🟡 [lab 03](../laboratorios/03-bigquery-parquet/README.md) |
| 12 | [`12-schedule-and-backfill-full-dataset.md`](12-schedule-and-backfill-full-dataset.md) | Programa el flujo de GCP y rellena todo el historial de taxis amarillos y verdes (`09_gcp_taxi_scheduled.yaml`). | 🔴 Requiere GCP · [apéndice](../docs/es/apendice-gcp.md) |
| 13 | [`13-why-ai-for-workflows.md`](13-why-ai-for-workflows.md) | Introducción breve a por qué la IA puede ahorrar trabajo al escribir flujos y por qué igual debes revisar lo que genera. | 🟢 Solo lectura |
| 14 | [`14-context-engineering-with-chatgpt.md`](14-context-engineering-with-chatgpt.md) | Un experimento: pedirle un flujo a un chat de IA sin darle contexto y observar los errores típicos (sintaxis vieja, propiedades inventadas). | 🔴 Cuenta externa (ChatGPT) |
| 15 | [`15-ai-copilot-in-kestra.md`](15-ai-copilot-in-kestra.md) | Activa el asistente de IA de Kestra con una clave de Gemini y compara su resultado con el del experimento anterior. | 🔴 Cuenta externa (clave de Gemini) |
| 16 | [`16-retrieval-augmented-generation.md`](16-retrieval-augmented-generation.md) | Explica RAG y lo prueba con dos flujos: uno que pregunta sin contexto (`10_chat_without_rag.yaml`) y otro que primero le da documentación al modelo (`11_chat_with_rag.yaml`). | 🔴 Cuenta externa (clave de Gemini) |
| 17 | [`17-deploy-to-the-cloud.md`](17-deploy-to-the-cloud.md) | Bonus opcional con enlaces para instalar Kestra en Google Cloud y sincronizar los flujos desde Git. | 🔴 Requiere GCP · [apéndice](../docs/es/apendice-gcp.md) |
| 18 | [`18-additional-resources.md`](18-additional-resources.md) | Enlaces a documentación y comunidad de Kestra, más consejos para resolver problemas: versiones fijas de las imágenes, choque de puertos y un error de BigQuery con archivos cortados. | 🟢 Solo lectura (los consejos de puertos te sirven en local) |

## Código y otros archivos

| Archivo o carpeta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice oficial del módulo, en inglés: lista de lecciones, resumen de cada sección y consejos de solución de problemas. | Para tener la vista general o revisar los consejos de errores. |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo: título, resumen y orden de las lecciones. La usa la plataforma del curso. | Casi nunca; no tienes que editarla. |
| [`docker-compose.yml`](docker-compose.yml) | Enciende cuatro servicios: Kestra (`localhost:8080`), su propia base Postgres, el Postgres de los taxis (`localhost:5432`) y pgAdmin (`localhost:8085`). El usuario y la clave de práctica de Kestra están en la sección `basicAuth`. | Desde la lección 03. Si ya tienes el Postgres del módulo 1 encendido, apágalo antes para que no choquen los puertos. |
| [`flows/01_hello_world.yaml`](flows/01_hello_world.yaml) a [`03_getting_started_data_pipeline.yaml`](flows/03_getting_started_data_pipeline.yaml) | Flujos introductorios: saludo con todos los conceptos, Python en contenedor y un *pipeline* pequeño con DuckDB. | Lecciones 04 a 06. 🟢 |
| [`flows/04_postgres_taxi.yaml`](flows/04_postgres_taxi.yaml), [`05_postgres_taxi_scheduled.yaml`](flows/05_postgres_taxi_scheduled.yaml) | Carga de taxis a Postgres, manual y programada. | Lecciones 07 y 08, y la tarea del módulo. 🟢 |
| [`flows/06_gcp_kv.yaml`](flows/06_gcp_kv.yaml) a [`09_gcp_taxi_scheduled.yaml`](flows/09_gcp_taxi_scheduled.yaml) | Configuración de GCP y carga de taxis a Cloud Storage y BigQuery. | Lecciones 10 a 12. 🔴 Requiere GCP |
| [`flows/10_chat_without_rag.yaml`](flows/10_chat_without_rag.yaml), [`11_chat_with_rag.yaml`](flows/11_chat_with_rag.yaml) | Flujos de IA que llaman a Gemini, sin y con RAG. | Lección 16. 🔴 Cuenta externa |
| [`images/`](images/) | Miniaturas de los videos y una imagen de la tarea. | No necesitas abrirlas. |

Un detalle práctico: la lección 15 indica entrar a una subcarpeta `docker` que en esta rama no existe; el `docker-compose.yml` está directamente en esta carpeta.

## Palabras en inglés que vas a encontrar

| Término | Qué significa |
|---|---|
| *workflow orchestration* | Orquestación: coordinar pasos de datos para que corran en orden y a tiempo. |
| *flow* | Flujo: el archivo YAML que describe un proceso completo en Kestra. |
| *task* | Tarea: cada paso dentro de un flujo (registrar un mensaje, correr SQL, descargar un archivo…). |
| *namespace* | Espacio de nombres: una especie de carpeta para ordenar flujos; aquí es `zoomcamp`. |
| *inputs* / *outputs* | Valores que eliges al ejecutar el flujo / resultados que una tarea entrega a la siguiente. |
| *trigger* / *schedule* | Disparador que inicia el flujo solo; el de tipo horario usa una expresión *cron*. |
| *execution* | Ejecución: cada vez que un flujo corre, con su estado y sus registros (*logs*). |
| *backfill* | Ejecutar el flujo para fechas pasadas, como si hubiera corrido en su momento. |
| *plugin* | Pieza de Kestra que sabe hacer un tipo de tarea, por ejemplo hablar con Postgres. |
| *KV Store* | Almacén de pares clave–valor de Kestra para guardar configuraciones. |
| *ETL* / *ELT* | Extraer, transformar y cargar / extraer, cargar y transformar después. |
| *data lake* / *data warehouse* | Lugar para guardar archivos crudos / base pensada para analizar grandes volúmenes. |
| *external table* | Tabla de BigQuery que lee directo desde archivos guardados en Cloud Storage. |
| *LLM* | Modelo de lenguaje grande, como los que están detrás de ChatGPT o Gemini. |
| *RAG* / *embeddings* | Técnica para darle documentos al modelo antes de que responda / números que representan el significado de un texto. |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la **cohorte 2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de la carpeta, preparada para 2027. En 2026 todo el módulo estaba en un solo `README.md` muy largo; ahora está dividido en 18 lecciones numeradas, con `module.yaml` y el video enlazado dentro de casi todas ellas. Los flujos de `flows/` y el `docker-compose.yml` no cambiaron, así que lo que practiques sirve igual. Lo único que desapareció es una extensión opcional de 2026 para cargar los datos FHV (otro tipo de vehículo) en GCP.

Los enlaces de las guías en español apuntan a la versión 2026 en GitHub. La tarea que usa la ruta es la de 2026, en [`../cohorts/2026/02-workflow-orchestration/homework.md`](../cohorts/2026/02-workflow-orchestration/homework.md); la de 2027 está en [`../cohorts/2027/homework/02-workflow-orchestration/homework.md`](../cohorts/2027/homework/02-workflow-orchestration/homework.md).
