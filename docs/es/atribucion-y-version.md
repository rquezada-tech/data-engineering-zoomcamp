# Atribución, licencias y versión de referencia

[Índice](../../README.md)

## Adaptación no oficial

Esta ruta es una **adaptación no oficial** del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp), creado por [DataTalks.Club](https://datatalks.club/) y su comunidad de instructores y colaboradores. **No** está afiliada a DataTalks.Club ni ha sido revisada por sus autores. Para el curso oficial, las inscripciones, las tareas y los certificados, usa siempre el [repositorio original](https://github.com/DataTalksClub/data-engineering-zoomcamp) y el [sitio del curso](https://datatalks.club/).

Este fork **no** envía cambios al repositorio original. La rama `main` del fork se mantiene idéntica a la del original.

## Versión de referencia

| Dato | Valor |
|---|---|
| Repositorio original | `DataTalksClub/data-engineering-zoomcamp` |
| Commit desde el que se creó la rama | [`813d2774083186d0c9705c920deaf3e6e1693335`](https://github.com/DataTalksClub/data-engineering-zoomcamp/commit/813d2774083186d0c9705c920deaf3e6e1693335) (`main` del 2026-11-16) |
| Commit de referencia del **contenido 2026** | [`a66ad5da2598d7ac147b37eec29632c93f4b1d9d`](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/a66ad5da2598d7ac147b37eec29632c93f4b1d9d) (2026-09-10) |
| Cohorte usada como base | 2026 (del 12 de enero al 11 de mayo de 2026) |
| Fecha de la adaptación | 2026-11-17 |

**¿Por qué dos commits?** El 2026-09-10, el repositorio original reemplazó el contenido de las carpetas de módulos (`01-docker-terraform/` … `07-streaming/`) por el de la **cohorte 2027**, en el commit `27d9cb3`. El commit `a66ad5d` es el último en que esas carpetas tenían el contenido de **2026**. Por eso, todos los enlaces de las guías apuntan a `a66ad5d`: así los videos, el material y las tareas que enlazamos son coherentes entre sí, aunque el repositorio original siga cambiando. Las tareas 2026 están, además, en `cohorts/2026/`.

## Licencias y reutilización

Revisamos los permisos antes de adaptar:

| Material | Licencia encontrada | Qué hicimos |
|---|---|---|
| Repositorio original en general | **No tiene un archivo de licencia** en la raíz; GitHub no detecta licencia | No copiamos ni tradujimos sus textos ni su código. Todas las guías, laboratorios, datos y ejercicios de `docs/es/` y `laboratorios/` son **originales** y enlazan el material oficial |
| `07-streaming/extras/pyflink/` | **MIT** (Copyright 2025 Sreela Das, Julie Scherer, Zach Wilson) | Solo se enlaza. El laboratorio de streaming de esta ruta es código propio y no copia ese ejemplo |
| Videos del curso | Publicados por DataTalks.Club en YouTube | Solo se enlazan |

Sin una licencia explícita, la reutilización de textos y código no está autorizada. Por eso esta ruta **explica con palabras propias** y **enlaza** el material original.

## Herramientas de terceros que usa la ruta

| Herramienta | Licencia | Nota |
|---|---|---|
| [LocalCloud](https://local.cloud/) | Propietaria, en "vista previa pública" | Gratis para uso individual y de código abierto al momento de escribir. Revisa los [términos vigentes](https://local.cloud/license/). La telemetría se desactiva en nuestro compose |
| PostgreSQL, Kestra, dlt, DuckDB, dbt Core, Bruin CLI, Apache Spark, Apache Flink, Redpanda, Streamlit | Cada una con su propia licencia | Se usan como dependencias, sin modificarlas |

## Datos

Todos los laboratorios usan **datos sintéticos** generados con semillas fijas: viajes, lecturas de sensores, pedidos y telemetría inventados. No se usan datos personales, datos de ninguna cuenta ni credenciales reales. Las claves que aparecen en los archivos `docker-compose.yml` y `.env.example` son **solo de práctica** y los servicios se publican únicamente en `127.0.0.1`.

## Licencia de esta adaptación

El repositorio original no declara una licencia, así que este fork tampoco agrega una licencia general. El contenido nuevo de `README.md`, `docs/es/` y `laboratorios/` lo escribió el autor de esta adaptación. En esta rama, el `README.md` original del curso se conserva sin cambios (salvo una línea inicial) como `README.en.md`; la rama `main` lo mantiene en su lugar original.
