# Clasificación de ejercicios

[Índice](../../README.es.md)

Esta tabla resume **dónde** se puede hacer cada parte del curso oficial (cohorte 2026) y cada laboratorio de esta ruta.

| Etiqueta | Significado |
|---|---|
| 🟢 **Local sin cambios** | Funciona igual que en el curso oficial, en tu Mac |
| 🟡 **Adaptado a local** | Funciona en tu Mac con LocalCloud u otra herramienta local; hay diferencias con la nube real que la guía explica |
| 🔴 **Requiere GCP** | Para reproducirlo fielmente necesitas Google Cloud (u otra cuenta externa); ver el [apéndice](apendice-gcp.md) |

## Laboratorios de esta ruta

| Laboratorio | Clasificación | ¿Probado? |
|---|---|---|
| [LocalCloud](../../laboratorios/localcloud/README.md) | 🟡 | ✅ |
| [01 · Docker + PostgreSQL](../../laboratorios/01-docker-postgres/README.md) | 🟢 | ✅ |
| [02 · Kestra](../../laboratorios/02-kestra/README.md) | 🟢 | ✅ Ejecución manual por API. Backfill y Schedule: no probados |
| [Taller dlt](../../laboratorios/taller-dlt/README.md) | 🟢 | ✅ |
| [03 · BigQuery + Parquet](../../laboratorios/03-bigquery-parquet/README.md) | 🟡 | ✅ Punta a punta, 2 veces, más pruebas de fallo |
| [04 · dbt + DuckDB](../../laboratorios/04-dbt-duckdb/README.md) | 🟡 | ✅ |
| [05 · Bruin](../../laboratorios/05-bruin/README.md) | 🟢 | ✅ |
| [06 · PySpark](../../laboratorios/06-pyspark/README.md) | 🟢 | ✅ |
| [07 · Redpanda + PyFlink](../../laboratorios/07-streaming/README.md) | 🟢 | ✅ |
| [Proyecto final](../../laboratorios/proyecto-final-telemetria/README.md) | 🟡 | ✅ Pipeline, pytest y dashboard |

El detalle de cada prueba está en el [registro de verificación](verificacion.md).

## Tareas oficiales 2026

| Módulo | Parte | Clasificación |
|---|---|---|
| 1 | Q1–Q2 (Docker, red de Compose) | 🟢 |
| 1 | Q3–Q6 (SQL sobre taxis verdes en PostgreSQL) | 🟢 |
| 1 | Q7 (flujo de Terraform) | 🔴 (la pregunta conceptual se responde con el apéndice) |
| 2 | Flujos 01–05 y preguntas (Postgres, scheduling, backfill) | 🟢 |
| 2 | Flujos 06–09 (GCS + BigQuery) | 🔴 |
| 2 | Flujos 10–11 (IA con Gemini) | 🔴 (cuenta externa) |
| Taller dlt | Pipeline desde la API del curso hacia DuckDB | 🟢 (requiere internet) |
| 3 | Q1, Q4 (conteos sobre tabla externa) | 🟡 |
| 3 | Q2, Q6, Q9 (bytes estimados) | 🔴 |
| 3 | Q3, Q5, Q7, Q8 (conceptuales y DDL) | 🟢 |
| 3 | BigQuery ML | 🔴 |
| 4 | Camino DuckDB + dbt Core y todas las preguntas | 🟢 |
| 4 | Camino BigQuery + dbt Cloud | 🔴 |
| 5 | Todas las preguntas (Bruin + DuckDB) | 🟢 |
| 5 | Bruin Cloud | 🔴 (cuenta externa, opcional) |
| 6 | Q1–Q6 (Spark local) | 🟢 |
| 6 | Spark con GCS, Dataproc y BigQuery | 🔴 |
| 7 | Q1–Q6 (Redpanda + PyFlink) | 🟢 |
| Proyecto | Criterio "nube" con puntaje completo | 🔴 |
| Proyecto | Resto de los criterios | 🟡 (ver el [ejemplo local](proyecto-final.md)) |
