# Mapa en español · 01-docker-terraform

[Índice de la ruta](../README.md) · [Mapa del curso](../docs/es/mapa-del-curso.md) · [Guía en español del módulo](../docs/es/modulo-01-docker-postgres.md)

> **Este archivo es una guía de lectura propia, no una traducción.** Todo el material de esta carpeta está en inglés y pertenece a [DataTalks.Club](https://datatalks.club/) y a sus autores. Aquí solo te contamos, con nuestras palabras, qué hay en cada archivo y para qué te sirve. Más detalles en [Atribución, licencias y versión de referencia](../docs/es/atribucion-y-version.md).

## En pocas palabras

Este es el primer módulo técnico del curso. Aprendes a usar **Docker** (una herramienta que empaqueta un programa con todo lo que necesita para que funcione igual en cualquier computador) y a levantar una base de datos **PostgreSQL** dentro de un contenedor. Después escribes en Python un proceso de **ingesta**, es decir, un programa que lee un archivo de datos (viajes de taxis de Nueva York) y lo guarda en la base. Al final repasas SQL y conoces **Terraform** y **Google Cloud (GCP)**, que sirven para crear infraestructura en la nube a partir de archivos de texto.

## Cómo recorrer esta carpeta

1. Lee primero la [guía en español del módulo 1](../docs/es/modulo-01-docker-postgres.md): explica los conceptos (imagen, contenedor, volumen, puerto, Compose) con ejemplos simples.
2. Haz el [laboratorio 01 · Docker + PostgreSQL](../laboratorios/01-docker-postgres/README.md). Usa datos inventados y te dice el resultado exacto que debes obtener, así sabes si lo hiciste bien.
3. Con esa base, recorre las lecciones `01` a `11` de esta carpeta en orden. Son la versión oficial del mismo camino, con los datos reales de taxis. Si el inglés se te hace pesado, apóyate en los comandos: casi todos se pueden copiar y ejecutar tal cual.
4. Las lecciones `12` y `13` (Terraform y GCP) necesitan una cuenta de Google Cloud. Léelas para entender la idea y usa el [apéndice de GCP](../docs/es/apendice-gcp.md) si algún día quieres hacerlas de verdad.

## Lecciones

| # | Lección | De qué trata | Dónde practicarlo |
|---|---|---|---|
| 01 | [`01-introduction.md`](01-introduction.md) | Qué es Docker y por qué se usa en datos. Muestra los primeros comandos (`docker run`, imágenes base, contenedores que se borran al salir) y cómo un volumen conecta una carpeta de tu computador con el contenedor. | 🟢 Local sin cambios · [lab 01](../laboratorios/01-docker-postgres/README.md) |
| 02 | [`02-virtual-environment.md`](02-virtual-environment.md) | Arma un primer *pipeline* pequeño con pandas y explica por qué conviene aislar las librerías de cada proyecto. Usa `uv` para crear el entorno y agregar dependencias. | 🟢 Local sin cambios |
| 03 | [`03-dockerizing-pipeline.md`](03-dockerizing-pipeline.md) | Escribe un `Dockerfile` para meter ese script en una imagen propia: primero con `pip` y luego con `uv`. | 🟢 Local sin cambios · [lab 01](../laboratorios/01-docker-postgres/README.md) |
| 04 | [`04-postgres-docker.md`](04-postgres-docker.md) | Levanta PostgreSQL 18 en un contenedor, compara dos formas de guardar sus datos (volumen con nombre o carpeta montada) y se conecta con `pgcli`. | 🟢 Local sin cambios · [lab 01](../laboratorios/01-docker-postgres/README.md) |
| 05 | [`05-data-ingestion.md`](05-data-ingestion.md) | En un cuaderno de Jupyter explora el CSV de taxis amarillos de enero de 2021, ajusta los tipos de columnas y lo carga a Postgres por partes (*chunks*) con pandas y SQLAlchemy. | 🟢 Local sin cambios (necesita internet para bajar el CSV) |
| 06 | [`06-ingestion-script.md`](06-ingestion-script.md) | Convierte el cuaderno en un script de Python (`ingest_data.py`) que recibe parámetros desde la terminal gracias a `click`. | 🟢 Local sin cambios |
| 07 | [`07-pgadmin.md`](07-pgadmin.md) | Agrega pgAdmin, una página web para explorar la base, y explica por qué dos contenedores necesitan estar en la misma red de Docker para verse. | 🟢 Local sin cambios · [lab 01](../laboratorios/01-docker-postgres/README.md) |
| 08 | [`08-dockerizing-ingestion.md`](08-dockerizing-ingestion.md) | Empaqueta el script de ingesta en una imagen y lo ejecuta como contenedor conectado a la red de Postgres. | 🟢 Local sin cambios |
| 09 | [`09-docker-compose.md`](09-docker-compose.md) | Reemplaza los comandos largos por un archivo de Docker Compose que enciende Postgres y pgAdmin juntos, y muestra cómo correr la ingesta contra esa red. | 🟢 Local sin cambios · [lab 01](../laboratorios/01-docker-postgres/README.md) |
| 10 | [`10-sql-refresher.md`](10-sql-refresher.md) | Repaso de SQL sobre los datos ya cargados: uniones entre tablas (`JOIN`), revisiones de calidad, agrupaciones y ordenamiento. Tiene video. | 🟢 Local sin cambios. Ojo: las consultas usan una tabla `zones` que las lecciones anteriores no enseñan a cargar; puedes adaptar el script de ingesta para hacerlo |
| 11 | [`11-cleanup.md`](11-cleanup.md) | Lista de comandos para borrar contenedores, imágenes, volúmenes, redes y archivos locales cuando terminas. Ojo con los comandos que borran todo. | 🟢 Local sin cambios |
| 12 | [`12-terraform-overview.md`](12-terraform-overview.md) | Presenta Terraform y la idea de "infraestructura como código": qué archivos usa, qué bloques declara y los cuatro comandos principales (`init`, `plan`, `apply`, `destroy`). | 🔴 Requiere GCP · [apéndice](../docs/es/apendice-gcp.md) (sección 1) |
| 13 | [`13-gcp-overview.md`](13-gcp-overview.md) | Pasos para abrir un proyecto en Google Cloud, crear una cuenta de servicio con sus permisos y dejar la autenticación lista para Terraform. | 🔴 Requiere GCP · [apéndice](../docs/es/apendice-gcp.md) |

## Código y otros archivos

| Archivo o carpeta | Qué es | Cuándo lo necesitas |
|---|---|---|
| [`README.md`](README.md) | Índice oficial del módulo, en inglés, con enlaces a las lecciones y apuntes de la comunidad. | Para ver la lista de lecciones o buscar apuntes de otros estudiantes. |
| [`module.yaml`](module.yaml) | Ficha técnica del módulo: título, resumen y orden de las lecciones. La usa la plataforma del curso. | Casi nunca; no tienes que editarla. |
| [`pipeline/`](pipeline/) | Código final de las lecciones 03 a 09: `Dockerfile`, `docker-compose.yaml`, `ingest_data.py`, `pyproject.toml` y `.python-version`. | Si te pierdes en las lecciones y quieres comparar con la versión terminada. El `Dockerfile` espera un archivo `uv.lock` que no viene incluido; se genera con `uv lock` dentro de la carpeta. |
| [`pipeline/docker-helper-scripts/`](pipeline/docker-helper-scripts/) | Tres scripts de terminal (`docker-postgres.sh`, `docker-pgadmin.sh`, `docker-ingest.sh`) con los comandos `docker run` largos ya escritos. | Para las lecciones 07 y 08, antes de pasar a Compose. Suponen que ya creaste la red `pg-network`. |
| [`setup/terraform-and-gcp-setup.md`](setup/terraform-and-gcp-setup.md) | Lista corta de requisitos para Terraform y GCP, con enlaces a las lecciones 12 y 13. | Solo si vas a usar GCP de verdad. |
| [`setup/terraform-on-windows.md`](setup/terraform-on-windows.md) | Instalación del SDK de Google Cloud y Terraform en Windows sin WSL. | No aplica en Mac. |
| [`terraform/README.md`](terraform/README.md) | Comandos para ejecutar los ejemplos de Terraform y una alternativa si tu organización no te deja crear llaves de cuenta de servicio. | Solo con cuenta de GCP. |
| [`terraform/terraform_basic/`](terraform/terraform_basic/) | Ejemplo mínimo en un solo `main.tf` que crea un *bucket* de Cloud Storage y un *dataset* de BigQuery. | 🔴 Requiere GCP. Sirve para leer cómo se ve un archivo de Terraform. |
| [`terraform/terraform_with_variables/`](terraform/terraform_with_variables/) | El mismo ejemplo, pero con los valores separados en `variables.tf`. | 🔴 Requiere GCP. |
| [`terraform/terraform_with_variable_AWS/`](terraform/terraform_with_variable_AWS/) | Aporte de la comunidad: una versión equivalente para Amazon Web Services (S3 y Glue). | 🔴 Requiere una cuenta de AWS. Opcional. |
| [`images/`](images/) | Diagramas (en `.png`, `.svg` y `.json`) y miniaturas de los videos. | No necesitas abrirlas; las lecciones ya las muestran. |

## Palabras en inglés que vas a encontrar

| Término | Qué significa |
|---|---|
| *container* | Contenedor: un programa corriendo aislado, con todo lo que necesita adentro. |
| *image* | Imagen: la "receta" congelada desde la que se crean contenedores. |
| *base image* | Imagen de partida sobre la que construyes la tuya, por ejemplo `python:3.13-slim`. |
| *volume* / *bind mount* | Dos formas de guardar datos fuera del contenedor para no perderlos al borrarlo. |
| *port mapping* | Conectar un puerto de tu computador con uno del contenedor (`-p 5432:5432`). |
| *network* | Red interna de Docker donde los contenedores se encuentran por nombre. |
| *virtual environment* | Entorno virtual: una carpeta con las librerías de un solo proyecto. |
| *pipeline* | Cadena de pasos que mueve y transforma datos. |
| *data ingestion* | Ingesta: llevar datos desde un archivo o sistema hasta una base de datos. |
| *chunk* | Trozo: una parte del archivo que se procesa de a una para no llenar la memoria. |
| *DDL / schema* | Instrucciones SQL que definen una tabla y sus columnas. |
| *Infrastructure as Code (IaC)* | Describir servidores, discos o bases en archivos de texto en vez de crearlos a mano. |
| *provider* | Complemento de Terraform que sabe hablar con una nube concreta (Google, AWS…). |
| *service account* | Cuenta "robot" de Google Cloud que usan los programas para autenticarse. |
| *bucket* | Contenedor de archivos en Cloud Storage; es el "lago de datos" del curso. |

## Ojo: versión 2027 vs versión 2026

La ruta en español se basa en la **cohorte 2026** (commit `a66ad5d`), pero esta rama trae la versión más nueva de la carpeta, preparada para 2027. El contenido es casi el mismo; lo que cambió es el orden. En 2026 las lecciones de Docker estaban dentro de la subcarpeta `docker-sql/` y las de Terraform y GCP dentro de `terraform/`. Ahora todo está numerado del `01` al `13` en la raíz, el código de la ingesta se movió de `docker-sql/pipeline/` a `pipeline/` sin cambios, los ejemplos de Terraform subieron un nivel y aparecieron `setup/` y `module.yaml`.

Los enlaces de las guías en español apuntan a la versión 2026 en GitHub, así que verás rutas como `docker-sql/...` que en esta rama ya no existen. La tarea que usa la ruta es la de 2026, en [`../cohorts/2026/01-docker-terraform/homework.md`](../cohorts/2026/01-docker-terraform/homework.md); la de 2027 está en [`../cohorts/2027/homework/01-docker-terraform/homework.md`](../cohorts/2027/homework/01-docker-terraform/homework.md).
