# Registro de verificación

[Índice](../../README.md)

Qué se probó al preparar esta ruta, cómo se hizo y con qué resultado. Si algo **no** se probó, se indica explícitamente. **Haber configurado algo no significa haberlo verificado.**

## Entorno de prueba

| Dato | Valor |
|---|---|
| Fecha | 2026-11-17 |
| Equipo | macOS con Apple Silicon (`uname -m` = `arm64`) |
| Docker | Docker Engine 29.9.2 (arm64), Docker Compose v5.6.1 |
| uv | 0.11.14 (binario x86_64 de Homebrew en `/usr/local`; ver [Antes de empezar](00-antes-de-empezar.md#42-tu-mac-usa-herramientas-arm64)) |
| Python de los laboratorios | 3.12 arm64 gestionado por uv. El laboratorio 3 también se probó con Python 3.12 x86_64 (Rosetta) |

## Verificaciones automáticas

### Validador de la ruta

```bash
uv run --no-project --with pyyaml python laboratorios/verificar_ruta.py
```

Revisa:

- **enlaces internos y anclas** de `README.md`, `docs/es/*.md` y los README de los laboratorios;
- que cada enlace al repositorio original exista en el commit de referencia `a66ad5d` (requiere el remoto `upstream`: `git remote add upstream https://github.com/DataTalksClub/data-engineering-zoomcamp.git && git fetch upstream`);
- `docker compose config` de cada `docker-compose.yml`;
- que todos los YAML se puedan leer y que todos los `.py` compilen.

Resultado: `RUTA OK ✅` (28 documentos, 187 enlaces internos, 35 enlaces al original, 5 archivos Compose, 18 YAML y 33 archivos Python).

El validador no revisa los enlaces **externos** (YouTube, documentación de terceros). El 2026-11-17 se revisaron aparte con `curl`: respondieron los 81 enlaces externos, después de corregir 2 que daban 404 (documentación de Bruin y de ventanas de Flink).

## Pruebas de punta a punta

| Laboratorio | Qué se ejecutó | Resultado |
|---|---|---|
| LocalCloud | `docker compose ... up -d --wait`, `/readiness`, `/env?format=shell`, consola web | ✅ Sano; BigQuery en `:5388` y GCS en `:5382`; consola HTTP 200 |
| 03 · BigQuery + Parquet | `./ejecutar_lab.sh` **tres veces**: dos en la copia de trabajo y una en un **clon limpio desde GitHub**, tras `down -v` de LocalCloud y siguiendo el inicio rápido del README | ✅ `LABORATORIO OK` las tres veces, con los mismos números |
| 03 · Seguridad | `BIGQUERY_EMULATOR_HOST=https://bigquery.googleapis.com` | ✅ Se detiene con un mensaje claro, código 2 |
| 03 · Seguridad | Resolución DNS de `bigquery.googleapis.com` con el bloqueo activo | ✅ Bloqueada |
| 03 · Seguridad | LocalCloud apagado (`docker stop localcloud`) | ✅ Mensaje claro con el comando para encenderlo, código 2, sin intentar Google |
| 03 · Persistencia | Reinicio del contenedor y `07_comprobar.py` | ✅ Los datos persisten en el volumen |
| 03 · Ejercicio de la guía | SQL de la solución y *dry run* | ✅ Aeropuerto 493.78, Puerto 357.07, 7,7 %; el emulador estima 193 555 B en ambas tablas |
| 01 · Docker + PostgreSQL | `up --wait`, `run --build ingesta` (2 veces), `consultas.sql`, pgAdmin | ✅ 3600 filas (sin duplicar al repetir); pgAdmin HTTP 200 a los ~20 s |
| 02 · Kestra | `cargar_flujos.sh`, `probar.sh` desde cero | ✅ 3 flujos en SUCCESS; 144 filas por día; reejecutar no duplica |
| 02 · Ejercicio de la guía | Tarea `Fail` agregada al flujo 3 | ✅ SUCCESS con 144; FAILED con el mensaje esperado si se piden 100 |
| Taller dlt | 3 ejecuciones (`--dias 3`, `5`, `5`) y `consultar.py` | ✅ 360 + 240 + 0 = 600 pedidos, 0 duplicados |
| 04 · dbt + DuckDB | `dbt build`, `dbt docs generate`/`serve` | ✅ PASS=24; docs HTTP 200 |
| 04 · Ejercicio de la guía | Modelo `viajes_por_tipo_pago` + prueba singular | ✅ PASS=23 (se retiraron después de probar) |
| 05 · Bruin | `validate`, `run`, `lineage`, `--var` | ✅ 4 assets y 13 controles OK; 4032 → 3931 filas; 318 alertas (641 con umbral 28) |
| 06 · PySpark | `generar_datos.py` y `trabajo_spark.py` con `spark-submit`; Spark UI | ✅ 50 000 → 49 483 filas; salida particionada por mes; UI HTTP 200 |
| 07 · Streaming | Construcción de la imagen de Flink en arm64, tópico, productor, consumidor, trabajo PyFlink, PostgreSQL | ✅ 50 filas (10 ventanas × 5 sensores); 45 con `--sin-cierre`; reconstrucción limpia OK |
| Proyecto final | `./ejecutar_proyecto.sh` en la copia de trabajo **y** en el clon limpio | ✅ `PIPELINE OK`, `3 passed` |
| Proyecto final · fallo controlado | `MAX_PCT_DESCARTADAS = 0.5` | ✅ Se detiene con código 2 y no calcula métricas |
| Proyecto final · dashboard | `AppTest` de Streamlit sin excepciones y revisión visual en el navegador | ✅ 4 indicadores, 2 gráficos, 2 tablas |

## Lo que NO se probó

Comandos documentados pero **no ejecutados** al preparar la ruta:

| Qué | Dónde está | Por qué |
|---|---|---|
| Backfill de Kestra desde la interfaz y el trigger `Schedule` activado | [Módulo 2](modulo-02-kestra.md) | Solo se probó la ejecución manual por API |
| Tarea oficial del módulo 3 con los ~20 millones de filas de taxis en LocalCloud | [Módulo 3](modulo-03-data-warehouse-bigquery.md) | Se probó el flujo con datos pequeños; el rendimiento a esa escala no se midió |
| Todo el [apéndice de GCP](apendice-gcp.md): Terraform, `gcloud storage cp`, `bq query --dry_run`, BigQuery ML, Dataproc, dbt Cloud | Apéndice | Requiere una cuenta de GCP con facturación |
| Terraform apuntando a LocalCloud con endpoints personalizados | Apéndice | Idea a explorar |
| Orquestar el proyecto final con Kestra (`host.docker.internal`) | [Proyecto final](proyecto-final.md#8-mejoras-sugeridas) | Propuesto como mejora |
| Ejercicios abiertos de las guías (dlt, Bruin, Spark, streaming) | Cada guía | Las soluciones se basan en el comportamiento probado de cada laboratorio, pero no todas se ejecutaron tal cual |
| Mac con chip Intel | — | La ruta está pensada para Apple Silicon |

## Cómo repetir la verificación

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down -v
```

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

```bash
(cd laboratorios/03-bigquery-parquet && ./ejecutar_lab.sh)
```

```bash
(cd laboratorios/proyecto-final-telemetria && ./ejecutar_proyecto.sh)
```

```bash
uv run --no-project --with pyyaml python laboratorios/verificar_ruta.py
```
