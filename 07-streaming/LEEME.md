# Mapa en español · 07-streaming

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-07-streaming.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo enseña **streaming**: procesar los datos a medida que llegan, en vez de esperar a juntarlos como en el módulo 6. El corazón es un taller práctico que arma, paso a paso, un pipeline completo: un programa en Python envía viajes de taxi como mensajes a **Redpanda** (un servidor de mensajes compatible con Kafka), **Apache Flink** los procesa de forma continua y los resultados quedan en **PostgreSQL**. En el camino aprendes qué son los tópicos, los offsets, las ventanas de tiempo y los watermarks. Todo corre en tu computador con Docker.

## Cómo recorrer esta carpeta

1. **Empieza en español:** lee la [guía del módulo 7](../docs/es/modulo-07-streaming.md) y haz el [laboratorio de Redpanda y PyFlink](../laboratorios/07-streaming/README.md). Usa lecturas de sensores en vez de taxis, pero las piezas son las mismas.
2. **Luego, el taller oficial (lecciones 01 a 13), en orden.** Cada lección agrega una pieza a la anterior, así que no conviene saltarse ninguna. Puedes escribir los archivos tú mismo o usar los que ya están listos en `code/`.
3. **La lección 14 (preguntas y respuestas)** sirve de repaso y para pensar cómo se usa Flink en una empresa.
4. **`theory/` y `extras/` son opcionales:** material de años anteriores. Míralos solo si quieres profundizar en Kafka.
5. **Para la tarea oficial 2026**, sigue la sección 8 de la guía. Todo el módulo funciona sin GCP.

## Lecciones

Las 14 lecciones forman un solo taller, que en la versión 2026 era un único documento largo (más detalles al final).

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [PyFlink: Stream Processing Workshop](01-introduction.md) | Presenta el taller, lo que vas a construir y las herramientas que necesitas (Docker, `uv` y un cliente de SQL). Enlaza el video y el código. | 🟢 Local sin cambios |
| 02 | [Redpanda - a Kafka-compatible broker](02-redpanda.md) | Explica qué es un *broker* de mensajes, por qué se usa Redpanda en vez de Kafka y cómo levantarlo con Docker Compose. | 🟢 Local sin cambios (también en el laboratorio) |
| 03 | [Produce messages to Kafka](03-produce-messages-to-kafka.md) | Crea el proyecto de Python, define cómo se ve cada viaje como mensaje y escribe el productor que los envía al tópico. | 🟢 Local sin cambios (descarga un Parquet público de taxis) |
| 04 | [Consume messages with Python](04-consume-messages-with-python.md) | Escribe un consumidor que lee los mensajes de vuelta, los convierte en objetos de Python y explica los grupos de consumidores. | 🟢 Local sin cambios (también en el laboratorio) |
| 05 | [Save events to PostgreSQL](05-save-events-to-postgresql.md) | Agrega PostgreSQL al Compose y modifica el consumidor para que guarde cada evento como una fila de una tabla. | 🟢 Local sin cambios |
| 06 | [Why Flink?](06-why-flink.md) | Lección corta que explica qué trabajo difícil te ahorra Flink frente a un consumidor hecho a mano y cuál es su costo. | 🟢 Local sin cambios (solo lectura) |
| 07 | [The Flink image and services](07-the-flink-image-and-services.md) | Construye una imagen de Docker de Flink con Python y conectores, y agrega al Compose sus dos servicios: el que coordina y el que ejecuta. | 🟢 Local sin cambios (usa los archivos de `code/`; ver la nota de abajo) |
| 08 | [The pass-through Flink job](08-the-pass-through-flink-job.md) | Primer trabajo de Flink: lee del tópico y copia cada evento a PostgreSQL, con puntos de control para recuperarse si falla. | 🟢 Local sin cambios |
| 09 | [Offsets - earliest vs latest](09-offsets-earliest-vs-latest.md) | Muestra la diferencia entre leer el tópico desde el principio o solo desde los mensajes nuevos, con un experimento. | 🟢 Local sin cambios (también en el laboratorio) |
| 10 | [Aggregation with tumbling windows](10-aggregation-with-tumbling-windows.md) | Cuenta viajes e ingresos por zona y por hora con ventanas fijas, y explica el watermark y la clave primaria para actualizar filas. | 🟢 Local sin cambios (el laboratorio hace lo mismo con ventanas de 1 minuto) |
| 11 | [Late events and upserts](11-late-events-and-upserts.md) | Usa un productor que inventa eventos con retrasos para ver cómo Flink corrige resultados ya publicados. | 🟢 Local sin cambios (usa `code/src/producers/producer_realtime.py`; ver la nota de abajo) |
| 12 | [Understanding window types](12-understanding-window-types.md) | Compara los tres tipos de ventana (fijas, deslizantes y de sesión) y para qué sirve cada una. | 🟢 Local sin cambios (la guía tiene un desafío con ventanas deslizantes) |
| 13 | [Cleanup](13-cleanup.md) | Cómo apagar los contenedores y, si quieres, borrar también los datos guardados. | 🟢 Local sin cambios |
| 14 | [Q&A](14-questions-and-answers.md) | Preguntas y respuestas de una transmisión de 2025: recuperación ante fallas, eventos muy atrasados, cuándo vale la pena el streaming y cómo se despliega en producción. | 🟢 Local sin cambios (solo lectura) |

> **Nota sobre las lecciones 07 y 11:** sus comandos `wget` descargan archivos desde una carpeta `07-streaming/workshop` del repositorio original que ya no existe, y la 07 menciona una ruta `cohorts/2027/07-streaming/code/` que tampoco existe. Los archivos que buscan están en [`code/`](code/) de esta misma carpeta: cópialos desde ahí.

## Código y otros archivos

| Ruta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) y [`module.yaml`](module.yaml) | Índice oficial del módulo y su ficha técnica para la plataforma del curso | El README, para ver el orden oficial; el `module.yaml` no lo necesitas |
| [`code/docker-compose.yml`](code/docker-compose.yml) | Levanta Redpanda, los dos servicios de Flink y PostgreSQL | Desde la lección 02; es la versión final de lo que construye el taller |
| [`code/Dockerfile.flink`](code/Dockerfile.flink), [`code/pyproject.flink.toml`](code/pyproject.flink.toml) y [`code/flink-config.yaml`](code/flink-config.yaml) | Receta de la imagen de Flink con Python, sus dependencias y su configuración | Lección 07 |
| [`code/Dockerfile_ARM64.flink`](code/Dockerfile_ARM64.flink) | Variante de la receta que instala herramientas extra para procesadores ARM64, como los Mac con Apple Silicon | Solo si la imagen normal no se construye en tu equipo; el Compose usa la otra por defecto |
| [`code/pyproject.toml`](code/pyproject.toml), `uv.lock` y `.python-version` | Dependencias de Python del productor y los consumidores, para `uv` | Lección 03 (`uv sync`) |
| [`code/Makefile`](code/Makefile) | Atajos para construir, levantar y apagar los servicios | Opcional. Su objetivo `job` apunta a un `start_job.py` que no está en esta carpeta; usa los comandos de las lecciones |
| [`code/src/models.py`](code/src/models.py) | Define cómo es un viaje y cómo se convierte de y hacia JSON | Lecciones 03 y 04 |
| [`code/src/producers/`](code/src/producers/) | `producer.py` (envía viajes reales) y `producer_realtime.py` (inventa viajes, algunos atrasados) | Lecciones 03 y 11 |
| [`code/src/consumers/`](code/src/consumers/) | `consumer.py` (muestra los mensajes) y `consumer_postgres.py` (los guarda en PostgreSQL) | Lecciones 04 y 05 |
| [`code/src/job/`](code/src/job/) | Trabajos de Flink: `pass_through_job.py`, `aggregation_job.py` y `aggregation_job_demo.py` (ventanas de 10 segundos para observar el watermark) | Lecciones 08 a 11 |
| [`code/live/`](code/live/) | El código escrito en vivo durante la transmisión del taller, con cuadernos de Jupyter en `notebooks/`. Su `README.md` está vacío | Solo para comparar con tu versión |
| [`theory/README.md`](theory/README.md) | Lista de videos antiguos (7.0.1 a 7.12) sobre conceptos de Kafka, Kafka Streams, ksqlDB y Schema Registry, con diagramas | Si quieres más teoría de Kafka; opcional |
| [`theory/java/kafka_examples/`](theory/java/kafka_examples/) | Ejemplos en Java de esos videos, configurados para Confluent Cloud | 🔴 Requiere una cuenta externa (Confluent Cloud); adaptarlo a Redpanda local no se probó |
| [`extras/extras/README.md`](extras/extras/README.md) | Índice de ejemplos de años anteriores | Opcional |
| [`extras/extras/python/`](extras/extras/python/) | Ejemplos en Python con varias librerías: JSON, Avro con Schema Registry, Redpanda, Faust y Spark Structured Streaming, más sus Compose | Opcional, para ver otras formas de producir y consumir |
| [`extras/extras/pyflink/`](extras/extras/pyflink/) | Un taller de PyFlink anterior (Flink 1.16, con `Makefile` y una tarea antigua en `homework.md`). **Tiene licencia MIT propia** ([`LICENSE`](extras/extras/pyflink/LICENSE)), de Sreela Das, Julie Scherer y Zach Wilson | Opcional; es la única parte de la carpeta con licencia explícita. Algunas rutas de su README ya no coinciden con la ubicación actual |
| [`extras/extras/ksqldb/commands.md`](extras/extras/ksqldb/commands.md) | Consultas de ejemplo en ksqlDB, un SQL que corre sobre tópicos de Kafka | Junto con el video de ksqlDB de `theory/` |
| `theory/images/` | Diagramas de la teoría (`.png` y su descripción en `.json`) | No hace falta abrirla: el README de `theory/` ya los muestra |

## Palabras en inglés que vas a encontrar

| Término | Qué significa |
|---|---|
| *stream processing* | Procesamiento en flujo: calcular sobre los datos apenas llegan |
| *broker* | Servidor que recibe, guarda y entrega mensajes; aquí, Redpanda |
| *topic* | Tópico: canal con nombre donde se guardan los mensajes de un tipo |
| *producer* / *consumer* | Programa que envía mensajes / programa que los lee |
| *consumer group* | Grupo de consumidores que se reparten un tópico y comparten su avance |
| *offset* | Posición de un mensaje dentro del tópico; `earliest` lee desde el principio y `latest` solo lo nuevo |
| *serializer* / *deserializer* | Funciones que convierten un objeto en bytes para enviarlo, y al revés |
| *JobManager* / *TaskManager* | En Flink: el servicio que coordina los trabajos / el que los ejecuta |
| *job* | Un trabajo de Flink que queda corriendo de forma continua |
| *checkpoint* | Foto periódica del estado de un trabajo para retomarlo si falla |
| *sink* | Destino donde un trabajo escribe sus resultados, como PostgreSQL |
| *tumbling* / *sliding* / *session window* | Ventana fija sin traslape / ventana deslizante que se traslapa / ventana que se cierra tras un rato sin eventos |
| *watermark* | Señal de Flink de "ya no espero eventos anteriores a esta hora" |
| *late event* | Evento atrasado, que llega después de lo esperado |
| *upsert* | Insertar una fila si no existe y actualizarla si ya existe |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la **cohorte 2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de la carpeta, preparada para 2027. En 2026, el taller completo era un solo archivo, `07-streaming/workshop/README.md`. Ahora ese archivo ya no existe: su contenido se dividió en las 14 lecciones de esta carpeta, en el mismo orden, y la carpeta `workshop/` pasó a llamarse `code/`, con los mismos archivos. Además, `extras/` quedó anidada un nivel más abajo (`extras/extras/`), por lo que algunos enlaces internos de su README ya no funcionan. Tampoco hay enlace a la tarea en el `README.md`: la tarea 2026 está en [`../cohorts/2026/07-streaming/homework.md`](../cohorts/2026/07-streaming/homework.md). Recuerda que los enlaces de las guías en español apuntan a la versión 2026, donde todavía existe `workshop/`.
