# Mapa en español · 05-data-platforms

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-05-bruin.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este módulo presenta las **plataformas de datos**: herramientas que reúnen en un solo lugar lo que antes hacías con varias (ingestar, transformar, orquestar, controlar la calidad y ver el linaje). El ejemplo es **Bruin**, una herramienta de línea de comandos que se configura con archivos YAML, SQL y Python. Vas a construir un pipeline de taxis de Nueva York en tres capas sobre **DuckDB** (una base de datos que corre en tu computador), y luego repasar uno por uno sus conceptos: proyectos, pipelines, assets, variables y comandos. Como extras, verás cómo usar Bruin con agentes de IA y cómo desplegar en su servicio en la nube.

## Cómo recorrer esta carpeta

1. Lee la [guía en español del módulo](../docs/es/modulo-05-bruin.md): explica proyecto, pipeline, asset, estrategias de materialización y controles de calidad.
2. Lee las lecciones 01 y 02 para instalar Bruin y entender cómo se ve un proyecto.
3. Haz el [laboratorio 05 · Bruin](../laboratorios/05-bruin/README.md): un pipeline pequeño con datos inventados de sensores que corre en local.
4. Sigue la lección 03 para armar el pipeline de taxis con la plantilla oficial (`bruin init zoomcamp …`). Necesitas internet para descargar los datos.
5. Usa las lecciones 06 a 10 como material de consulta: son cortas y cada una explica un concepto.
6. Las lecciones 04 (MCP) y 05 (Bruin Cloud) son opcionales.
7. Para la tarea, usa la de la cohorte 2026: [`../cohorts/2026/05-data-platforms/homework.md`](../cohorts/2026/05-data-platforms/homework.md).

## Lecciones

Leyenda: 🟢 local sin cambios · 🟡 adaptado a local · 🔴 requiere GCP o cuenta externa.

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [Introduction to Bruin](01-introduction.md) | Qué es Bruin, qué piezas suele tener un stack de datos moderno y qué vas a aprender en la serie. | 🟢 Conceptual |
| 02 | [Getting Started with Bruin](02-getting-started.md) | Instalación, extensión para el editor, creación de un proyecto con `bruin init`, los archivos `.bruin.yml` y `pipeline.yml`, los tipos de asset y los comandos básicos. | 🟢 Local con DuckDB (el ejemplo descarga datos de una API pública) |
| 03 | [Building an End-to-End Pipeline with NYC Taxi Data](03-nyc-taxi-pipeline.md) | Construye paso a paso el pipeline de taxis en tres capas (ingesta, staging y reportes) sobre DuckDB, y resume las estrategias de materialización. | 🟢 Local con DuckDB; necesita internet · laboratorio 05 |
| 04 | [Using Bruin MCP with AI Agents](04-bruin-mcp.md) | Cómo conectar Bruin a un asistente de IA en el editor (Cursor, VS Code o Claude Code) para que construya el pipeline y responda preguntas sobre los datos. | 🟢 Opcional; el asistente de IA puede pedir su propia cuenta |
| 05 | [Deploying to Bruin Cloud](05-bruin-cloud.md) | Registro en el servicio en la nube de Bruin, conexión con tu repositorio de GitHub, configuración de conexiones, despliegue y monitoreo. | 🔴 Cuenta externa (opcional) |
| 06 | [Core Concepts: Projects](06-core-concepts-projects.md) | Qué es un proyecto de Bruin y cómo `.bruin.yml` define entornos y conexiones. | 🟢 Laboratorio 05 |
| 07 | [Core Concepts: Pipelines](07-core-concepts-pipelines.md) | Qué es un pipeline, por qué tiene una sola programación y qué se configura en `pipeline.yml`. | 🟢 Laboratorio 05 |
| 08 | [Core Concepts: Assets](08-core-concepts-assets.md) | Los tipos de asset (SQL, Python y seed), cómo se nombran, cómo se materializan y cómo se ejecuta uno solo o con lo que depende de él. | 🟢 Laboratorio 05 |
| 09 | [Core Concepts: Variables](09-core-concepts-variables.md) | Variables que Bruin entrega por defecto (como las fechas de inicio y fin) y variables propias que puedes cambiar al ejecutar con `--var`. | 🟢 Laboratorio 05 |
| 10 | [Core Concepts: Commands](10-core-concepts-commands.md) | Los comandos principales (`bruin run`, `bruin validate`, `bruin lineage`, `bruin query`) y sus opciones más usadas. | 🟢 Laboratorio 05 |

## Código y otros archivos

Esta carpeta **no trae código**: el pipeline de taxis se genera con la plantilla de Bruin (`bruin init zoomcamp <carpeta>`) y las lecciones muestran el contenido de cada archivo.

| Archivo o carpeta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice del módulo con la lista de lecciones y un espacio para apuntes de la comunidad. | Para orientarte; la sección de tarea está vacía en esta versión. |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo que usa la plataforma del curso. | Casi nunca. |
| `images/` | Diagramas del proyecto, del pipeline y del linaje (en `.png`, `.svg` y su fuente `.json`) y miniaturas de los videos. | No necesitas abrirla: las lecciones ya muestran las imágenes. |

## Palabras en inglés que vas a encontrar

| Término | Significado sencillo |
|---|---|
| Data platform | Plataforma de datos: una herramienta que cubre todo el ciclo, de la ingesta al reporte. |
| Project | Carpeta raíz de Bruin; contiene `.bruin.yml` con las conexiones. |
| Pipeline | Grupo de assets que se ejecutan juntos con una misma programación. |
| Asset | Cada pieza de datos que produce el pipeline: una tabla, una vista o un archivo. |
| Ingestion / ingestor | Ingesta: traer datos desde una fuente externa hacia tu base de datos. |
| Seed | Archivo CSV que se carga como tabla. |
| Materialization strategy | Cómo se escribe la tabla en cada ejecución: reemplazarla, agregar filas, reescribir un rango de fechas… |
| Quality check | Control de calidad: regla que se verifica después de crear un asset. |
| Lineage | Linaje: el diagrama de qué asset depende de cuál. |
| Upstream / downstream | Lo que va antes (de lo que dependes) y lo que va después (lo que depende de ti). |
| Full refresh | Reconstruir todo desde cero en vez de procesar solo lo nuevo. |
| Environment / connection | Entorno (por ejemplo, desarrollo o producción) y datos de acceso a una base de datos. |
| MCP | *Model Context Protocol*: forma estándar de dar herramientas a un asistente de IA. |
| Deploy | Desplegar: publicar el pipeline para que se ejecute en un servidor. |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la cohorte **2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de esta carpeta. En 2026 el `README.md` era una página larga de videos con un resumen de cada uno y apuntes en la subcarpeta `notes/` (por ejemplo `notes/06-core-01-projects.md`); ahora esos apuntes están en la raíz como `01-…md` a `10-…md`, con diagramas nuevos, y el `README.md` es un índice corto sin el enlace directo a la plantilla de Bruin ni a la tarea. El contenido de las lecciones casi no cambió. **Los enlaces de las guías en español apuntan a la versión 2026**, así que allá verás las rutas con `notes/`.
