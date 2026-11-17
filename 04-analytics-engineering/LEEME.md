# Mapa en español · 04-analytics-engineering

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-04-dbt-duckdb.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo enseña **analytics engineering**: el trabajo de convertir datos crudos en tablas limpias, confiables y listas para reportes. La herramienta es **dbt** (*data build tool*), que ejecuta consultas `SELECT` organizadas en capas dentro de tu base de datos, con pruebas automáticas y documentación. Vas a construir el proyecto `taxi_rides_ny` con viajes de taxis de Nueva York, desde los datos crudos hasta tablas de hechos, dimensiones y un reporte mensual. El curso ofrece dos caminos: **DuckDB + dbt Core** (local y gratis) o **BigQuery + dbt Cloud** (en la nube).

## Cómo recorrer esta carpeta

1. Lee la [guía en español del módulo](../docs/es/modulo-04-dbt-duckdb.md) para tener el mapa mental: capas, `ref()`, `source()`, hechos y dimensiones.
2. Si el SQL te cuesta, repasa antes [`refreshers/SQL.md`](refreshers/SQL.md) (funciones de ventana y CTE).
3. Lee las lecciones 01 a 03: son conceptuales y no requieren instalar nada.
4. Haz el [laboratorio 04 · dbt + DuckDB](../laboratorios/04-dbt-duckdb/README.md): un proyecto dbt pequeño, con datos inventados, que corre en minutos.
5. Con esa base, sigue las lecciones 04 a 11 junto al proyecto [`taxi_rides_ny/`](taxi_rides_ny/), usando el camino local de [`setup/local_setup.md`](setup/local_setup.md). Ese camino descarga varios GB de datos reales.
6. Para la tarea, usa la de la cohorte 2026: [`../cohorts/2026/04-analytics-engineering/homework.md`](../cohorts/2026/04-analytics-engineering/homework.md).

## Lecciones

Leyenda: 🟢 local sin cambios · 🟡 adaptado a local · 🔴 requiere GCP o cuenta externa.

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [Analytics Engineering Basics](01-analytics-engineering-basics.md) | Por qué surgió el rol de analytics engineer, la diferencia entre ETL y ELT, y las ideas básicas del modelado dimensional: tablas de hechos, tablas de dimensión y esquema estrella. | 🟢 Conceptual |
| 02 | [What is dbt?](02-what-is-dbt.md) | Qué es dbt, qué problemas resuelve, cómo transforma un `SELECT` en una tabla o vista, y los dos caminos de instalación que ofrece el curso. | 🟢 Conceptual |
| 03 | [dbt Core vs dbt Cloud](03-dbt-core-vs-dbt-cloud.md) | Compara la versión gratuita de línea de comandos con la plataforma web administrada (dbt Cloud, que pide crear una cuenta), menciona el nuevo motor dbt Fusion y explica qué camino recomienda el curso. | 🟢 Conceptual. Usar dbt Cloud: 🔴 |
| 04 | [dbt Project Structure](04-dbt-project-structure.md) | Recorre las carpetas y archivos que crea `dbt init` y cómo se reparten los modelos en `staging`, `intermediate` y `marts`. | 🟢 DuckDB + dbt Core · laboratorio 04 |
| 05 | [dbt Sources](05-dbt-sources.md) | Cómo declarar en `sources.yml` dónde están los datos crudos y cómo escribir los primeros modelos de staging: renombrar columnas y fijar tipos. | 🟢 DuckDB + dbt Core · laboratorio 04 |
| 06 | [dbt Models](06-dbt-models.md) | Diferencia entre `source()` y `ref()`, para qué sirve la capa intermedia y cómo unir los viajes de taxis verdes y amarillos aunque sus columnas no sean iguales. | 🟢 DuckDB + dbt Core · laboratorio 04 |
| 07 | [dbt Seeds and Macros](07-dbt-seeds-and-macros.md) | Cargar tablas de consulta desde CSV (seeds) y reemplazar código repetido por macros reutilizables; adelanta parte de la tarea. | 🟢 DuckDB + dbt Core · laboratorio 04 |
| 08 | [Documentation](08-documentation.md) | Cómo describir fuentes, modelos y columnas en archivos YAML y cómo generar y abrir el sitio web de documentación de dbt. | 🟢 `dbt docs generate` y `dbt docs serve` funcionan en local |
| 09 | [dbt Tests](09-dbt-tests.md) | Repasa todos los tipos de prueba de dbt: singulares, de frescura de las fuentes, genéricas (incluidas y propias), pruebas unitarias y contratos de modelo. | 🟢 DuckDB + dbt Core · laboratorio 04 |
| 10 | [dbt Packages](10-dbt-packages.md) | Presenta paquetes útiles de la comunidad, como `dbt_utils` y `codegen`, y cómo instalarlos con `packages.yml` y `dbt deps`. | 🟢 Local (necesita internet para descargar los paquetes) |
| 11 | [dbt Commands](11-dbt-commands.md) | Resumen de los comandos de dbt (`dbt run`, `dbt test`, `dbt build`, `dbt retry`…) y de las opciones más útiles, como `--select` y `--full-refresh`. | 🟢 DuckDB + dbt Core · laboratorio 04 |

> El laboratorio 04 de esta ruta está marcado 🟡 porque reemplaza BigQuery por DuckDB, pero el camino local del curso oficial (DuckDB + dbt Core) es 🟢. Lo que exige BigQuery o dbt Cloud es 🔴: revisa el [apéndice de GCP](../docs/es/apendice-gcp.md).

## Código y otros archivos

| Archivo o carpeta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice del módulo: lista de lecciones, guías de instalación, archivos de apoyo y apuntes de la comunidad. | Para orientarte; la sección de tarea está vacía en esta versión. |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo que usa la plataforma del curso. | Casi nunca. |
| [`setup/local_setup.md`](setup/local_setup.md) | Paso a paso del camino local: instalar DuckDB y dbt, configurar `~/.dbt/profiles.yml`, descargar los datos y la extensión dbt Power User para VS Code. | Antes de la lección 04 si sigues el proyecto oficial. 🟢 |
| [`setup/duckdb_troubleshooting.md`](setup/duckdb_troubleshooting.md) | Qué hacer si DuckDB se queda sin memoria: ajustar límites, `dbt retry`, construir por partes. | Si tu computador tiene poca RAM o el `dbt build` falla. 🟢 |
| [`setup/cloud_setup.md`](setup/cloud_setup.md) | Paso a paso del camino en la nube: cuenta de servicio de GCP, registro en dbt Cloud y conexión a BigQuery. | Solo si tienes GCP y cuenta de dbt Cloud. 🔴 |
| [`refreshers/SQL.md`](refreshers/SQL.md) | Repaso de SQL: funciones de ventana (`ROW_NUMBER`, `RANK`, `LAG`…) y CTE. | Antes de las lecciones de modelos si el SQL avanzado te resulta nuevo. |
| [`taxi_rides_ny/`](taxi_rides_ny/) | El proyecto dbt completo que se construye en el módulo. | Como referencia mientras sigues las lecciones 04 a 11. |
| `taxi_rides_ny/dbt_project.yml` | Configuración del proyecto: nombre, carpetas, variables y si cada capa se guarda como vista o tabla. | Lección 04. |
| `taxi_rides_ny/models/` | Modelos SQL y YAML en tres capas: `staging/` (con `sources.yml`), `intermediate/` y `marts/` (con `reporting/`). | Lecciones 05 a 09. |
| `taxi_rides_ny/seeds/` | CSV de consulta: zonas de taxi y tipos de pago, con su YAML de propiedades. | Lección 07. |
| `taxi_rides_ny/macros/` | Macros: duración del viaje en minutos, nombre del proveedor y conversión segura de tipos. | Lección 07. |
| `taxi_rides_ny/packages.yml` y `package-lock.yml` | Lista de paquetes externos y sus versiones fijadas. | Lección 10 (`dbt deps`). |
| `taxi_rides_ny/snapshots/` y `tests/` | Carpetas vacías (solo `.gitkeep`) para que tú agregues snapshots y pruebas singulares. | Lección 09 y ejercicios propios. |
| `images/` | Diagramas (con sus fuentes `.json`) y miniaturas de los videos. | No necesitas abrirla. |

## Palabras en inglés que vas a encontrar

| Término | Significado sencillo |
|---|---|
| Analytics engineer | Persona entre ingeniería de datos y análisis que modela y prueba los datos para reportes. |
| ETL / ELT | Extraer, transformar y cargar; en ELT primero se carga y luego se transforma dentro del almacén. |
| Model | En dbt, un archivo `.sql` con un `SELECT` que se convierte en tabla o vista. |
| Source | Datos crudos que dbt no crea y solo lee. |
| Staging / intermediate / marts | Capas: limpieza básica, reglas intermedias y tablas finales para el negocio. |
| Fact table / dimension table | Tabla de hechos (eventos medibles) y tabla de dimensión (descripciones). |
| Star schema | Esquema estrella: hechos al centro y dimensiones alrededor. |
| Seed | Archivo CSV pequeño que dbt carga como tabla. |
| Macro | Función reutilizable escrita con Jinja que genera SQL. |
| Materialization | Forma de guardar un modelo: vista, tabla, incremental… |
| Lineage | Linaje: el diagrama de qué modelo depende de cuál. |
| Data test / unit test | Regla que verifica los datos / prueba que verifica la lógica con datos de ejemplo. |
| Freshness | Frescura: qué tan recientes son los datos de una fuente. |
| Profile (`profiles.yml`) | Archivo con los datos de conexión a tu base de datos. |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la cohorte **2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de esta carpeta. El cambio principal es de organización: los apuntes que en 2026 vivían en `class_notes/` (por ejemplo `4_3_2_dbt_sources.md`) ahora están en la raíz como `01-…md` a `11-…md`, con pequeños retoques y diagramas nuevos, y el `README.md` pasó de ser una página de videos con requisitos y caminos de instalación a un índice corto con la tarea vacía. El proyecto `taxi_rides_ny/` y las guías de `setup/` no cambiaron. **Los enlaces de las guías en español apuntan a la versión 2026**, así que allá verás los nombres de archivo antiguos.
