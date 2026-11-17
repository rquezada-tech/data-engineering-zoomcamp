# Mapa del curso original (en inglés)

[Índice](../../README.md) · [Glosario](glosario.md)

> **Qué es esto:** una guía de lectura, en español, para moverte por las carpetas del curso original de [DataTalks.Club](https://datatalks.club/), que están en inglés. **No es una traducción**: el repositorio original no tiene licencia, así que sus textos no se pueden traducir ni republicar sin permiso. Lo que sí hacemos es explicarte, con nuestras palabras, qué hay en cada carpeta, para qué sirve y qué guía en español cubre ese tema. Más detalles en [Atribución, licencias y versión de referencia](atribucion-y-version.md).

---

## Cómo usar este mapa

1. **Aprende primero en español.** Cada módulo tiene una guía en `docs/es/` y un laboratorio que funciona en tu Mac. Empieza siempre por ahí.
2. **Usa el material original como complemento.** Cuando quieras ver los videos, revisar el código del curso o hacer la tarea oficial, abre el mapa de esa carpeta (`LEEME.md`). Te dice qué archivo abrir, de qué trata y si se puede hacer en local.
3. **No te asustes con el inglés.** Cada mapa incluye una tabla con las palabras en inglés que vas a encontrar en esa carpeta. El [glosario](glosario.md) explica los conceptos generales.

> 💡 **Truco:** en GitHub, al abrir una carpeta, se muestra su `README.md` en inglés. Busca el archivo `LEEME.md` en la lista de archivos de esa misma carpeta para ver el mapa en español.

## Los módulos

| Módulo | Carpeta original (inglés) | Mapa en español | Guía en español | Laboratorio local |
|---|---|---|---|---|
| 1 · Docker, SQL y Terraform | [`01-docker-terraform/`](../../01-docker-terraform/) | [LEEME](../../01-docker-terraform/LEEME.md) | [Docker y PostgreSQL](modulo-01-docker-postgres.md) | [01-docker-postgres](../../laboratorios/01-docker-postgres/README.md) |
| 2 · Orquestación | [`02-workflow-orchestration/`](../../02-workflow-orchestration/) | [LEEME](../../02-workflow-orchestration/LEEME.md) | [Kestra](modulo-02-kestra.md) | [02-kestra](../../laboratorios/02-kestra/README.md) |
| 3 · Data warehouse | [`03-data-warehouse/`](../../03-data-warehouse/) | [LEEME](../../03-data-warehouse/LEEME.md) | [BigQuery](modulo-03-data-warehouse-bigquery.md) | [03-bigquery-parquet](../../laboratorios/03-bigquery-parquet/README.md) |
| 4 · Analytics engineering | [`04-analytics-engineering/`](../../04-analytics-engineering/) | [LEEME](../../04-analytics-engineering/LEEME.md) | [dbt y DuckDB](modulo-04-dbt-duckdb.md) | [04-dbt-duckdb](../../laboratorios/04-dbt-duckdb/README.md) |
| 5 · Plataformas de datos | [`05-data-platforms/`](../../05-data-platforms/) | [LEEME](../../05-data-platforms/LEEME.md) | [Bruin](modulo-05-bruin.md) | [05-bruin](../../laboratorios/05-bruin/README.md) |
| 6 · Procesamiento batch | [`06-batch/`](../../06-batch/) | [LEEME](../../06-batch/LEEME.md) | [PySpark](modulo-06-pyspark.md) | [06-pyspark](../../laboratorios/06-pyspark/README.md) |
| 7 · Streaming | [`07-streaming/`](../../07-streaming/) | [LEEME](../../07-streaming/LEEME.md) | [Redpanda y PyFlink](modulo-07-streaming.md) | [07-streaming](../../laboratorios/07-streaming/README.md) |

## Cohortes, tareas y proyecto

| Carpeta original | Mapa en español | Para qué la vas a usar |
|---|---|---|
| [`cohorts/`](../../cohorts/) | [LEEME](../../cohorts/LEEME.md) | Cada año del curso (2022 a 2027) con sus tareas y su proyecto |
| [`cohorts/2026/`](../../cohorts/2026/) | [LEEME](../../cohorts/2026/LEEME.md) | La edición en la que se basa esta ruta: tareas de cada módulo y del proyecto |
| [`projects/`](../../projects/) | [LEEME](../../projects/LEEME.md) | Cómo funciona el proyecto final y qué datos puedes usar. Nuestra versión local está en [Proyecto final](proyecto-final.md) |

## Otros archivos de la raíz

Estos archivos no forman parte de ningún módulo. Algunos te sirven como estudiante y otros son para quienes mantienen el curso.

| Archivo o carpeta | Qué es | ¿Te sirve? |
|---|---|---|
| [`README.en.md`](../../README.en.md) | Portada original del curso, en inglés: presentación, calendario, módulos e instructores | Sí, para ver la información oficial del curso |
| [`awesome-data-engineering.md`](../../awesome-data-engineering.md) | Lista de recursos externos: cursos, libros, blogs y herramientas, ordenados por tema | Sí, cuando termines la ruta y quieras profundizar |
| [`certificates.md`](../../certificates.md) | Cómo se obtiene el certificado del curso y cómo agregarlo a LinkedIn | Solo si te inscribes en una cohorte oficial y entregas el proyecto |
| [`workshop-best-practices.md`](../../workshop-best-practices.md) | Recomendaciones para quienes **preparan** talleres del curso: ritmo, datos, estructura del código | No como estudiante; es para autores de talleres |
| [`course.yaml`](../../course.yaml) | Archivo de configuración que lista las cohortes y dónde está el contenido de cada una. Lo usa la plataforma del curso | No; es para la plataforma |
| [`images/`](../../images/) | Imágenes de la portada: diagramas de arquitectura y logos de patrocinadores | No directamente |
| [`scripts/`](../../scripts/) | Herramienta interna que genera las miniaturas de los videos | No; es para mantener el repositorio |
| `.tmp/` | Notas de trabajo internas de los mantenedores sobre cambios de imágenes de la versión 2027 | No |
| `.github/` | Configuración de GitHub del repositorio original (por ejemplo, el botón de patrocinio) | No |

## Versión 2026 y versión 2027

El curso se actualiza cada año. Esta ruta en español se basa en la **cohorte 2026**, pero esta rama parte del estado más reciente del repositorio original, que ya trae la **versión 2027** en las carpetas de los módulos.

- **Las guías en español** enlazan siempre a la versión 2026 (commit `a66ad5d`), para que videos y tareas coincidan con lo que explicamos.
- **Las carpetas de esta rama** muestran la versión 2027. Cada mapa tiene una sección "Ojo: versión 2027 vs versión 2026" que explica qué cambió.
- **El material de la cohorte 2026** también está en esta rama, en [`cohorts/2026/`](../../cohorts/2026/).

[Índice](../../README.md) · [Glosario](glosario.md)
