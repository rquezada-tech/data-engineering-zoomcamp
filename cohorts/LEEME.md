# Mapa en español · cohorts

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md)

> **Guía de lectura propia, no una traducción.** Este archivo te ayuda a orientarte dentro de la carpeta `cohorts/`. Todo el material que hay aquí está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/). Para saber qué se adaptó, con qué permisos y desde qué versión, lee [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## ¿Qué es una cohorte?

El Data Engineering Zoomcamp se dicta **una vez al año**, en vivo, con fecha de inicio y de término. A cada una de esas ediciones se le llama **cohorte** (en inglés, *cohort*): el grupo de personas que hace el curso al mismo tiempo, con el mismo calendario.

Cada cohorte tiene su propia carpeta con el año como nombre (`cohorts/2026/`, por ejemplo). Ahí vas a encontrar lo que cambia de un año a otro:

- **Fechas** del curso y plazos de entrega.
- **Tareas** (*homework*): un cuestionario por módulo que se responde en un formulario del sitio del curso.
- **Proyecto final** (`project.md`): cómo y cuándo se entrega ese año.
- **Talleres** (*workshops*): sesiones extra con invitados, cuando las hubo.

Las **lecciones** (videos y apuntes) no siempre están aquí: en general viven en las carpetas de módulos de la raíz (`01-docker-terraform/` … `07-streaming/`). La carpeta de la cohorte guarda sobre todo lo que se evalúa.

## ¿Qué hay en cada año?

| Año | Fechas | Qué módulos y herramientas | Tareas | Proyecto | Talleres y extras |
|---|---|---|---|---|---|
| [2022](2022/) | 17 ene – 9 may 2022 | Carpetas `week_N_*` (semanas). Docker, Terraform y GCP; ingesta y orquestación con Airflow; data warehouse; procesamiento batch con Spark; streaming con Kafka | Sí, en las semanas 1, 2, 5 y 6 (no hay carpeta de la semana 4) | Sí (`project.md`) | Sin talleres. Enlace a la tabla de posiciones dentro del `README.md` |
| [2023](2023/) | 16 ene – 11 may 2023 | Carpetas `week_N_*`. La semana 1 trae dos tareas (Docker/SQL y Terraform); orquestación con Prefect; BigQuery; dbt; Spark; Kafka | Sí, en las 6 semanas | Sí, con dos intentos | Taller de PipeRider + dbt (`workshops/piperider.md`) y `leaderboard.md` |
| [2024](2024/) | 15 ene – 28 may 2024 | Ahora se llaman **módulos** `01` a `06`. Orquestación con Mage; dbt; Spark; streaming con Kafka/Redpanda y Spark | Sí, en los 6 módulos | Sí | Talleres de dlt (ingesta) y RisingWave (streaming en SQL). `leaderboard.md` |
| [2025](2025/) | 13 ene – 5 may 2025 | Módulos `01` a `06`. Orquestación con Kestra; BigQuery; dbt; Spark; streaming con Redpanda y PyFlink | Sí, en los 6 módulos | Sí | Taller de dlt con su propia tarea (`workshops/dlt/`) |
| [2026](2026/) | 12 ene – 11 may 2026 | Módulos `01` a `07`: aparece el módulo **05 · Data Platforms** con Bruin; batch pasa a ser el 06 y streaming el 07 | Sí, en los 7 módulos | Sí, con dos intentos | Taller de dlt asistido por IA, con tarea. Ver el [mapa de 2026](2026/LEEME.md) |
| [2027](2027/) | 11 ene – 5 abr 2027 (provisorias) | Mismos 7 módulos que 2026, ya reorganizados en la raíz del repositorio | Sí, pero son **borradores** marcados `[DRAFT]` copiados de 2026 | Sí (`project.md`) | Aún no publicada (`published: false`). Incluye una nota interna sobre el reemplazo de diagramas |

> Las cohortes 2022 a 2026 son **archivos históricos**: quedaron congeladas tal como se dictaron. Por eso los nombres de carpetas cambian de un año a otro. La única cohorte "viva" es 2027, que todavía es un borrador.

## ¿Qué cohorte usa la ruta en español?

La ruta en español se basa en la **cohorte 2026**, tomando como referencia el commit `a66ad5d` del repositorio original. Las razones:

1. **Es la última edición completa y publicada.** Tiene tareas reales, plazos, soluciones de algunos módulos y proyecto con dos intentos. La de 2027 todavía es un borrador.
2. **El contenido cambia con el tiempo.** El 10 de septiembre de 2026 el repositorio original reemplazó las carpetas de módulos de la raíz por el material de 2027. El commit `a66ad5d` es la última "foto" en que esas carpetas tenían el contenido de 2026.
3. **Coherencia.** Al fijar ese commit, los videos, apuntes y tareas que enlazan las guías de `docs/es/` corresponden todos al mismo año.

Un *commit* es una versión guardada del repositorio en un momento dado; su código corto (como `a66ad5d`) sirve para volver a verla exactamente igual. Los detalles están en [Atribución y versión](../docs/es/atribucion-y-version.md).

## Cómo encontrar la tarea de un módulo

La tarea siempre está en un archivo llamado `homework.md`, pero la ruta cambia según el año:

| Año | Dónde buscar | Ejemplo |
|---|---|---|
| 2022 | `cohorts/2022/week_N_<tema>/homework.md` (la semana 2 está dentro de una subcarpeta `homework/`) | [`2022/week_5_batch_processing/homework.md`](2022/week_5_batch_processing/homework.md) |
| 2023 | `cohorts/2023/week_N_<tema>/homework.md` | [`2023/week_4_analytics_engineering/homework.md`](2023/week_4_analytics_engineering/homework.md) |
| 2024 y 2025 | `cohorts/<año>/0N-<módulo>/homework.md` | [`2025/02-workflow-orchestration/homework.md`](2025/02-workflow-orchestration/homework.md) |
| 2026 | `cohorts/2026/0N-<módulo>/homework.md` | [`2026/05-data-platforms/homework.md`](2026/05-data-platforms/homework.md) |
| 2027 | `cohorts/2027/homework/0N-<módulo>/homework.md`, más un `homework.yaml` con los datos de la tarea | [`2027/homework/01-docker-terraform/homework.md`](2027/homework/01-docker-terraform/homework.md) |

Consejos:

- El camino más corto es abrir el `README.md` de la cohorte: lista cada módulo con un enlace llamado **Homework**.
- Las tareas de los **talleres** están dentro de `workshops/` (por ejemplo, `2026/workshops/dlt/dlt_homework.md`).
- Algunas carpetas incluyen `solutions.md` con las respuestas. Intenta resolver la tarea antes de mirarlas.
- Las tareas de años anteriores sirven como **práctica extra**, pero sus formularios ya están cerrados.

## Otros archivos de esta carpeta

| Archivo | Para qué sirve |
|---|---|
| [`README.md`](README.md) | Explica (en inglés) cómo se organiza el repositorio: el contenido actual vive en la raíz y cada cohorte guarda solo fechas y tareas |
| `<año>/cohort.yaml` | Ficha técnica de cada cohorte que lee el sitio web del curso. En el [mapa de 2026](2026/LEEME.md) se explica campo por campo |
| `<año>/README.md` | Calendario y enlaces de esa edición: videos de lanzamiento, preguntas frecuentes, tareas y proyecto |
| `<año>/project.md` | Cómo se entregaba el proyecto final ese año |

## Palabras en inglés que vas a encontrar

| Palabra | Qué significa aquí |
|---|---|
| *cohort* | Cohorte: la edición de un año del curso |
| *homework* | Tarea del módulo; se responde en un formulario |
| *week* / *module* | Semana / módulo: las unidades del curso (2022–2023 hablaban de semanas) |
| *deadline* | Fecha límite para entregar |
| *submission form* | Formulario de entrega |
| *solution* | Solución oficial publicada después del plazo |
| *leaderboard* | Tabla de posiciones con el puntaje de cada participante |
| *workshop* | Taller extra, normalmente con una empresa o herramienta invitada |
| *office hours* | Sesión en vivo de preguntas y respuestas |
| *peer review* | Revisión entre pares: tus compañeros evalúan tu proyecto y tú el de ellos |
| *attempt* | Intento: el proyecto se puede entregar en dos rondas |
| *draft* | Borrador: contenido que todavía puede cambiar |
| *launch stream* | Transmisión en vivo con la que arranca la cohorte |
| *FAQ* | Preguntas frecuentes |
