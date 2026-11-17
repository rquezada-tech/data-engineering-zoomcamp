# Data Engineering Zoomcamp en español · Ruta local para Mac

> **Adaptación no oficial** del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) de [DataTalks.Club](https://datatalks.club/), basada en la **cohorte 2026**. Todo el crédito del curso original es de sus autores. Más detalles en [Atribución, licencias y versión de referencia](docs/es/atribucion-y-version.md). El README original en inglés está en [README.en.md](README.en.md).

Una ruta para aprender **ingeniería de datos desde cero**, en español latinoamericano, que puedes seguir **completa en tu Mac** sin cuenta ni facturación de Google Cloud.

- 📖 **Guías pensadas para quien recién empieza**: cada concepto se explica con ejemplos cotidianos antes de tocar código.
- 💻 **Laboratorios que funcionan en local**, probados en macOS con Apple Silicon, con datos inventados y resultados esperados exactos para que sepas si lo hiciste bien.
- ☁️ **BigQuery y Cloud Storage emulados** con [LocalCloud](https://local.cloud/). Lo que de verdad requiere Google Cloud está en un [apéndice opcional](docs/es/apendice-gcp.md).

---

## ¿Por dónde empiezo?

1. Lee **[Antes de empezar](docs/es/00-antes-de-empezar.md)**: qué es la ingeniería de datos y cómo preparar tu Mac (Docker, uv, git).
2. Enciende **[LocalCloud](docs/es/localcloud.md)**, tu "Google Cloud de bolsillo".
3. Sigue los módulos **en orden**. Cada guía te dice qué problema resuelve, qué vas a construir, cómo ejecutarlo, qué resultado esperar y cómo comprobarlo.

## Inicio rápido

Si ya tienes Docker Desktop y `uv` instalados, estos comandos encienden el emulador y corren el laboratorio de BigQuery completo:

```bash
git clone https://github.com/rquezada-tech/data-engineering-zoomcamp.git
```

```bash
cd data-engineering-zoomcamp && git switch adaptacion-es-localcloud
```

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

```bash
cd laboratorios/03-bigquery-parquet && ./ejecutar_lab.sh
```

Si al final ves `LABORATORIO OK ✅`, tu entorno funciona. Para apagar el emulador, vuelve a la raíz del repositorio y ejecuta:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down
```

## La ruta

| # | Guía | Qué aprendes | Laboratorio | Dónde corre |
|---|---|---|---|---|
| 0 | [Antes de empezar](docs/es/00-antes-de-empezar.md) | Qué hace una persona ingeniera de datos; preparar el Mac | — | — |
| 0 | [LocalCloud](docs/es/localcloud.md) | Qué es un emulador y cómo usar BigQuery y GCS en local | [localcloud](laboratorios/localcloud/README.md) | 🟡 |
| 1 | [Docker y PostgreSQL](docs/es/modulo-01-docker-postgres.md) | Contenedores, Compose, ingesta por trozos | [01-docker-postgres](laboratorios/01-docker-postgres/README.md) | 🟢 |
| 2 | [Orquestación con Kestra](docs/es/modulo-02-kestra.md) | Flujos, triggers, backfill, idempotencia | [02-kestra](laboratorios/02-kestra/README.md) | 🟢 |
| — | [Taller: ingesta con dlt](docs/es/taller-dlt.md) | APIs, normalización, carga incremental | [taller-dlt](laboratorios/taller-dlt/README.md) | 🟢 |
| 3 | [Data warehouse con BigQuery](docs/es/modulo-03-data-warehouse-bigquery.md) | Lago vs almacén, Parquet, tablas externas, partición, clustering | [03-bigquery-parquet](laboratorios/03-bigquery-parquet/README.md) | 🟡 |
| 4 | [Analytics engineering con dbt y DuckDB](docs/es/modulo-04-dbt-duckdb.md) | Modelos en capas, hechos y dimensiones, pruebas | [04-dbt-duckdb](laboratorios/04-dbt-duckdb/README.md) | 🟡 |
| 5 | [Plataformas de datos con Bruin](docs/es/modulo-05-bruin.md) | Assets, controles de calidad, linaje, variables | [05-bruin](laboratorios/05-bruin/README.md) | 🟢 |
| 6 | [Batch con PySpark](docs/es/modulo-06-pyspark.md) | Procesamiento distribuido, DataFrames, shuffle | [06-pyspark](laboratorios/06-pyspark/README.md) | 🟢 |
| 7 | [Streaming con Redpanda y PyFlink](docs/es/modulo-07-streaming.md) | Tópicos, ventanas, watermarks | [07-streaming](laboratorios/07-streaming/README.md) | 🟢 |
| ★ | [Proyecto final: telemetría de dispositivos](docs/es/proyecto-final.md) | Pipeline completo con calidad, métricas de disponibilidad y dashboard | [proyecto-final-telemetria](laboratorios/proyecto-final-telemetria/README.md) | 🟡 |
| + | [Apéndice: lo que requiere GCP](docs/es/apendice-gcp.md) | Terraform, Compute Engine, bytes reales, BigQuery ML | — | 🔴 |

🟢 local sin cambios · 🟡 adaptado a local · 🔴 requiere GCP. Detalle por ejercicio en **[Clasificación de ejercicios](docs/es/clasificacion-ejercicios.md)**.

## Material de apoyo

- 📚 [Glosario](docs/es/glosario.md): todos los términos explicados en simple.
- ✅ [Registro de verificación](docs/es/verificacion.md): qué se probó, cómo y con qué resultado.
- 🏷️ [Atribución, licencias y versión de referencia](docs/es/atribucion-y-version.md).
- 🎥 [Lista de videos oficial del curso (en inglés)](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) y [FAQ oficial](https://datatalks.club/faq/data-engineering-zoomcamp.html).

## Requisitos

- Mac con Apple Silicon (M1 o superior). Recomendado: 16 GB de RAM y 30 GB libres en disco.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) con 6 a 8 GB de memoria asignada.
- [uv](https://docs.astral.sh/uv/) y git: `brew install uv git`.
- Conocimientos básicos de Python y SQL. No necesitas experiencia previa en datos.

## Convenciones

- Los comandos, nombres de APIs, funciones e identificadores técnicos se dejan en su forma original (`docker compose`, `SELECT`, `bigquery.Client`).
- Los enlaces al material oficial apuntan al commit [`a66ad5d`](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/a66ad5da2598d7ac147b37eec29632c93f4b1d9d), el último con el contenido de la cohorte 2026.
- Ningún laboratorio se conecta a Google Cloud real. Los que usan LocalCloud **bloquean** cualquier conexión a `*.googleapis.com`.

---

¿Buscas el curso oficial en inglés? Está en el [README original](README.md).
