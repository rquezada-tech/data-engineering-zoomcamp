# Mapa en español · projects

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md)

> **Guía de lectura propia, no una traducción.** Este archivo te orienta dentro de la carpeta `projects/`. Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/). Para saber qué se adaptó, con qué permisos y desde qué versión, lee [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## ¿Qué es el proyecto final?

Es el cierre del curso. Después de los módulos, tienes unas tres semanas para construir **tu propio pipeline de datos de punta a punta**: un recorrido completo que toma datos de una fuente, los guarda, los transforma y termina en un **dashboard** (un tablero con gráficos) que responde alguna pregunta.

Un *pipeline* es una cadena de pasos automáticos por la que pasan los datos, como una línea de producción en una fábrica. El proyecto te pide armar todos los eslabones, no solo uno.

Las piezas típicas son:

| Paso | Qué haces | Módulo donde lo aprendes |
|---|---|---|
| Elegir datos | Buscas un conjunto de datos que te interese | — |
| Ingesta | Llevas esos datos a un **lago de datos** (almacenamiento de archivos crudos), por lotes (*batch*) o en tiempo real (*stream*) | 1, 2, taller dlt, 7 |
| Warehouse | Los pasas a un **data warehouse** (base de datos pensada para análisis) | 3 |
| Transformación | Los limpias y preparas para responder preguntas | 4, 5, 6 |
| Dashboard | Muestras el resultado en al menos dos gráficos | — |

Reglas importantes que conviene saber desde el principio:

- **No puedes usar los datos de taxis de Nueva York**, porque se usan en todo el curso. Tienes que elegir otro conjunto de datos.
- Puedes usar herramientas que no se vieron en el curso, siempre que expliques qué hacen.
- Copiar un proyecto ajeno, o reutilizar uno tuyo de otro curso, se considera plagio y anula el puntaje.
- Se recomienda crear un **repositorio nuevo** solo para el proyecto, con un `README.md` bien detallado: es lo primero que verán quienes lo evalúen y también te sirve como portafolio.

## ¿Cómo se evalúa?

No lo corrige un profesor: lo revisan **tres compañeros** de la misma cohorte, con una rúbrica común. A eso se le llama **revisión entre pares** (*peer review*). En resumen:

- La rúbrica tiene siete áreas: qué tan claro está el problema, uso de la nube (y de infraestructura como código), ingesta (batch o streaming), diseño del warehouse, transformaciones, dashboard y reproducibilidad (que otra persona pueda correrlo siguiendo tus instrucciones).
- Cada área recibe 0, 2 o 4 puntos, según qué tan completa esté.
- Para que tu proyecto cuente, **tú también debes evaluar tres proyectos** de otras personas. Cada evaluación que haces suma puntos a tu nota.
- En las cohortes recientes hay **dos intentos** de entrega: si no alcanzas el primero o no lo apruebas, puedes presentarte al segundo.
- Hay sugerencias opcionales para destacar (pruebas automáticas, `make`, CI/CD) que no se califican.

La rúbrica exacta y las fechas están en inglés en [`README.md`](README.md) y en el `project.md` de cada cohorte (por ejemplo, [`cohorts/2026/project.md`](../cohorts/2026/project.md)). En la [guía del proyecto final](../docs/es/proyecto-final.md) hay una tabla que explica cada criterio con un ejemplo.

## Qué hay en esta carpeta

| Archivo | Qué contiene |
|---|---|
| [`README.md`](README.md) | La descripción oficial del proyecto: objetivo, qué entregar, tecnologías permitidas, dashboard, rúbrica de evaluación, reglas de plagio, consejos de revisores anteriores, enlaces útiles y la galería de proyectos de la comunidad |
| [`datasets.md`](datasets.md) | Una lista de sitios donde buscar datos para tu proyecto (ver abajo) |

### `datasets.md`

Es un listado de **fuentes de datos públicas** para inspirarte. Incluye:

- Catálogos generales y buscadores de datos (Kaggle, el buscador de Google, colecciones "awesome" de datos públicos).
- Datos abiertos de gobiernos y organismos (Reino Unido, estadísticas europeas, NASA, clima de NOAA).
- Conjuntos que ofrecen las nubes (AWS, Azure, BigQuery y otros servicios de GCP).
- Datos temáticos: música, actividad de GitHub, bicicletas de Londres, alimentos, criptomonedas, una copia de la web (Common Crawl) y opciones pensadas para streaming.

No es obligatorio usar uno de esa lista: cualquier conjunto de datos sirve, menos el de taxis. Antes de elegir, revisa que tenga **fechas** y **categorías**, porque el dashboard pide un gráfico en el tiempo y otro por categoría.

## Cómo se relaciona con la ruta en español

| Material | Para qué te sirve |
|---|---|
| [`README.md`](README.md) de esta carpeta | Las reglas oficiales. Es la referencia que usarán tus revisores |
| [`docs/es/proyecto-final.md`](../docs/es/proyecto-final.md) | Guía en español: resume qué pide el curso, explica cada criterio, muestra un ejemplo completo y te da pasos para armar tu propio proyecto |
| [`laboratorios/proyecto-final-telemetria/`](../laboratorios/proyecto-final-telemetria/README.md) | Un **proyecto de ejemplo** que puedes ejecutar en tu Mac: telemetría inventada de 12 dispositivos, lago y warehouse emulados con LocalCloud, controles de calidad, métricas de disponibilidad y un dashboard en Streamlit |
| [`docs/es/clasificacion-ejercicios.md`](../docs/es/clasificacion-ejercicios.md) | Te dice qué criterios puedes cumplir en local y cuál necesita una nube real |
| [`docs/es/apendice-gcp.md`](../docs/es/apendice-gcp.md) | Qué hacer si quieres el puntaje completo en el criterio de nube |

Ten en cuenta dos cosas:

1. **El ejemplo es una referencia, no una entrega.** Úsalo para entender la estructura y las decisiones, pero elige tu propio problema y tus propios datos.
2. **Local no es lo mismo que nube.** El ejemplo emula BigQuery y Cloud Storage en tu computador. Eso alcanza para aprender y para casi toda la rúbrica, pero el criterio de nube solo da el puntaje máximo si despliegas en una nube real con infraestructura como código.

## Palabras en inglés que vas a encontrar

| Palabra | Qué significa aquí |
|---|---|
| *project* / *capstone* | Proyecto final del curso |
| *end-to-end* | De punta a punta: desde la fuente de datos hasta el dashboard |
| *dataset* | Conjunto de datos |
| *data lake* | Lago de datos: almacenamiento de archivos tal como llegan |
| *data warehouse* (DWH) | Base de datos pensada para consultas de análisis |
| *batch* / *stream* | Procesar por lotes cada cierto tiempo / procesar en tiempo real |
| *dashboard* / *tile* | Tablero con gráficos / cada gráfico del tablero |
| *IaC* (*Infrastructure as Code*) | Crear la infraestructura de la nube con archivos de código, como Terraform |
| *reproducibility* | Que otra persona pueda ejecutar tu proyecto y obtener lo mismo |
| *peer review* / *peers* | Revisión entre compañeros / tus compañeros de cohorte |
| *evaluation criteria* | Criterios de evaluación (la rúbrica) |
| *attempt* | Intento de entrega |
| *deadline* | Fecha límite |
| *plagiarism* | Plagio |
