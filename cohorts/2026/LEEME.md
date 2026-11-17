# Mapa en español · cohorts/2026

[Índice de la ruta](../../README.md) · [Mapa del curso](../../docs/es/mapa-del-curso.md) · [Todas las cohortes](../LEEME.md)

> **Guía de lectura propia, no una traducción.** Este archivo te orienta dentro de `cohorts/2026/`. Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/). Para saber qué se adaptó, con qué permisos y desde qué versión, lee [Atribución, licencias y versión de referencia](../../docs/es/atribucion-y-version.md).

## La cohorte 2026 en pocas palabras

La edición 2026 del curso se dictó del **12 de enero al 11 de mayo de 2026**. Tuvo **7 módulos**, un taller de ingesta con dlt y un proyecto final con dos intentos de entrega. Es la cohorte en la que se basa toda la ruta en español.

Esta carpeta guarda **lo que se evaluaba** ese año: las tareas (*homework*), algunas soluciones, el taller y las reglas de entrega del proyecto. Las **lecciones** (videos y apuntes) de 2026 estaban en las carpetas de módulos de la raíz en el commit `a66ad5d`; hoy esas carpetas tienen el material de 2027. Las guías en español enlazan siempre a esa versión de 2026.

## Módulo por módulo

Cada fila une la tarea oficial (en inglés) con la guía y el laboratorio en español que te preparan para ella.

| # | Tema y herramientas | Tarea oficial | Guía en español | Laboratorio |
|---|---|---|---|---|
| 1 | Contenedores con Docker, SQL en PostgreSQL e infraestructura como código con Terraform | [`01-docker-terraform/homework.md`](01-docker-terraform/homework.md) | [Módulo 1 · Docker y PostgreSQL](../../docs/es/modulo-01-docker-postgres.md) | [01-docker-postgres](../../laboratorios/01-docker-postgres/README.md) |
| 2 | Orquestación de flujos con Kestra (carga de datos de taxis, programación y *backfill*) | [`02-workflow-orchestration/homework.md`](02-workflow-orchestration/homework.md) | [Módulo 2 · Kestra](../../docs/es/modulo-02-kestra.md) | [02-kestra](../../laboratorios/02-kestra/README.md) |
| Taller | Ingesta desde una API con dlt hacia DuckDB, con ayuda de un asistente de IA | [`workshops/dlt/dlt_homework.md`](workshops/dlt/dlt_homework.md) | [Taller dlt](../../docs/es/taller-dlt.md) | [taller-dlt](../../laboratorios/taller-dlt/README.md) |
| 3 | Data warehouse con BigQuery y Cloud Storage: tablas externas, particiones, *clustering* | [`03-data-warehouse/homework.md`](03-data-warehouse/homework.md) | [Módulo 3 · BigQuery](../../docs/es/modulo-03-data-warehouse-bigquery.md) | [03-bigquery-parquet](../../laboratorios/03-bigquery-parquet/README.md) |
| 4 | *Analytics engineering* con dbt: modelos en capas y pruebas | [`04-analytics-engineering/homework.md`](04-analytics-engineering/homework.md) | [Módulo 4 · dbt y DuckDB](../../docs/es/modulo-04-dbt-duckdb.md) | [04-dbt-duckdb](../../laboratorios/04-dbt-duckdb/README.md) |
| 5 | Plataformas de datos con Bruin: un pipeline completo con controles de calidad | [`05-data-platforms/homework.md`](05-data-platforms/homework.md) | [Módulo 5 · Bruin](../../docs/es/modulo-05-bruin.md) | [05-bruin](../../laboratorios/05-bruin/README.md) |
| 6 | Procesamiento *batch* con Spark (PySpark) | [`06-batch/homework.md`](06-batch/homework.md) | [Módulo 6 · PySpark](../../docs/es/modulo-06-pyspark.md) | [06-pyspark](../../laboratorios/06-pyspark/README.md) |
| 7 | *Streaming* con Redpanda (compatible con Kafka) y PyFlink | [`07-streaming/homework.md`](07-streaming/homework.md) | [Módulo 7 · Streaming](../../docs/es/modulo-07-streaming.md) | [07-streaming](../../laboratorios/07-streaming/README.md) |
| ★ | Proyecto final: un pipeline de punta a punta con datos que eliges tú | [`project.md`](project.md) | [Proyecto final](../../docs/es/proyecto-final.md) | [proyecto-final-telemetria](../../laboratorios/proyecto-final-telemetria/README.md) |

Archivos extra dentro de los módulos:

- `03-data-warehouse/` trae un script de Python y un notebook para subir los datos de la tarea a la nube.
- `06-batch/solutions.md` y `07-streaming/solutions/` contienen **soluciones oficiales**. Resuelve la tarea primero y úsalas solo para comparar.
- Algunas tareas enlazan carpetas de la raíz con rutas relativas (por ejemplo, `07-streaming/workshop/`). Como la raíz ya tiene el material de 2027, esos enlaces pueden fallar aquí: búscalos en el commit `a66ad5d` del repositorio original.

## ¿Qué puedes hacer en tu Mac?

Resumen de la [clasificación de ejercicios](../../docs/es/clasificacion-ejercicios.md). Las etiquetas significan: 🟢 funciona en local igual que en el curso, 🟡 funciona en local con un emulador (con diferencias explicadas en la guía), 🔴 necesita Google Cloud u otra cuenta externa.

| Módulo | En local | Qué necesita la nube |
|---|---|---|
| 1 | 🟢 Docker, red de Compose y las consultas SQL | 🔴 La pregunta de Terraform se responde leyendo el [apéndice GCP](../../docs/es/apendice-gcp.md) |
| 2 | 🟢 Flujos con PostgreSQL, programación y *backfill* | 🔴 Flujos que usan GCS/BigQuery y los de IA con Gemini |
| Taller dlt | 🟢 Todo (necesitas internet para leer la API) | — |
| 3 | 🟢 Preguntas conceptuales y de DDL · 🟡 conteos sobre tablas externas con LocalCloud | 🔴 Bytes estimados por BigQuery y BigQuery ML |
| 4 | 🟢 Todas las preguntas, por el camino DuckDB + dbt Core | 🔴 El camino BigQuery + dbt Cloud |
| 5 | 🟢 Todas las preguntas con Bruin + DuckDB | 🔴 Bruin Cloud (opcional) |
| 6 | 🟢 Todas las preguntas con Spark local | 🔴 Spark con GCS, Dataproc y BigQuery |
| 7 | 🟢 Todas las preguntas con Redpanda + PyFlink en Docker | — |
| Proyecto | 🟡 Casi todos los criterios ([ejemplo local](../../docs/es/proyecto-final.md)) | 🔴 El puntaje completo del criterio de nube |

## Qué es cada archivo de esta carpeta

| Archivo o carpeta | Qué contiene |
|---|---|
| [`README.md`](README.md) | El calendario de la cohorte: videos de lanzamiento, preguntas frecuentes, lista de reproducción y un enlace a la tarea de cada módulo |
| [`cohort.yaml`](cohort.yaml) | Ficha técnica de la cohorte (ver abajo) |
| [`project.md`](project.md) | Reglas de entrega del proyecto 2026: dos intentos, formularios de entrega y de revisión, y el aviso para actualizar tu nombre en el certificado. Los criterios de evaluación están en [`projects/`](../../projects/LEEME.md) |
| `0N-<módulo>/` | Una carpeta por módulo con su `homework.md` y, en algunos casos, soluciones o scripts de apoyo |
| [`workshops/`](workshops/) | El taller de dlt (ver abajo) |

### `cohort.yaml`, campo por campo

Un archivo YAML es un texto con pares `clave: valor` que leen los programas. Este en particular lo usa el sitio web del curso para saber qué mostrar.

| Campo | Qué dice |
|---|---|
| `schema_version` | Versión del formato del archivo |
| `content_id` | Identificador único interno de la cohorte |
| `identifier` | El nombre corto de la cohorte: `"2026"` |
| `course` | A qué curso pertenece: `de-zoomcamp` |
| `delivery: live` | Se dictó en vivo, con calendario |
| `published: true` | Está publicada en el sitio |
| `start_date` / `end_date` | Inicio (2026-01-12) y término (2026-05-11) |
| `curriculum: github_archive` | Es un archivo histórico congelado: no se edita como contenido actual |
| `archive.notice_path` | Qué archivo mostrar como portada del archivo histórico (`README.md`) |
| `homework: []` | Lista vacía: las tareas de 2026 no se registran aquí, sino como archivos dentro de cada carpeta de módulo |

### `workshops/`

| Archivo | Qué contiene |
|---|---|
| [`workshops/dlt.md`](workshops/dlt.md) | Ficha del taller: video, de qué trata, quién lo dictó y enlaces a materiales y al formulario de la tarea |
| [`workshops/dlt/README.md`](workshops/dlt/README.md) | Instrucciones paso a paso: crear un pipeline con dlt que lee una API pública de libros y guarda en DuckDB, ayudándote de un editor con IA |
| [`workshops/dlt/dlt_homework.md`](workshops/dlt/dlt_homework.md) | La tarea del taller: armar tu propio pipeline contra una API de viajes de taxi y responder preguntas sobre los datos |
| `workshops/dlt/*.py`, `*.ipynb`, `pyproject.toml` | Código y notebook de ejemplo del taller |

En el `README.md` de la cohorte el taller aparece dos veces (como "Workshop 1" y "Workshop 2"), pero ambos enlaces llevan a este mismo material de dlt.

## Palabras en inglés que vas a encontrar

| Palabra | Qué significa aquí |
|---|---|
| *homework* | Tarea del módulo, con preguntas de opción múltiple o respuesta corta |
| *question* | Cada pregunta de la tarea (Q1, Q2…) |
| *submitting the solutions* | Sección que explica cómo entregar las respuestas |
| *submission form* | Formulario de entrega en el sitio del curso |
| *deadline* | Fecha límite |
| *learning in public* | Aprender en público: la invitación, al final de cada tarea, a compartir en redes lo que aprendiste |
| *workshop* | Taller extra con una herramienta invitada |
| *setup* | Preparación del entorno antes de empezar |
| *backfill* | Ejecutar un flujo para fechas pasadas que no se procesaron |
| *solution* | Solución oficial |
| *attempt* | Intento de entrega del proyecto (hay dos) |
| *peer review* / *review* | Revisión de proyectos entre compañeros |
| *certificate name* | El nombre que aparecerá en tu certificado |
| *office hours* | Sesión en vivo de preguntas y respuestas |
