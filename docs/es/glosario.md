# Glosario

[Índice](../../README.es.md)

Términos que aparecen en la ruta, explicados en simple. Entre paréntesis va el módulo donde se usan más.

| Término | Qué significa |
|---|---|
| **API** | Un servicio al que un programa le pide datos por internet, siguiendo reglas fijas. (taller dlt) |
| **Backfill** | Ejecutar un flujo para fechas pasadas, "como si" hubiera corrido en esos días. (2) |
| **Batch (lotes)** | Procesar datos acumulados cada cierto tiempo, por ejemplo cada noche. (6) |
| **Broker** | Servidor que recibe, guarda y entrega mensajes, como Redpanda o Kafka. (7) |
| **Bucket** | "Bodega" de archivos en Cloud Storage. Dirección: `gs://nombre/carpeta/archivo`. (3) |
| **Chunk (trozo)** | Una porción de un archivo grande que se procesa por separado para no llenar la memoria. (1) |
| **Clustering** | Ordenar las filas de una tabla por ciertas columnas para leer menos al filtrar. (3) |
| **Contenedor** | Un programa empaquetado con todo lo que necesita, aislado del resto del sistema. (1) |
| **Cron** | Formato de texto para decir "cuándo" se repite algo: `0 6 * * *` = todos los días a las 6:00. (2) |
| **CTAS** | `CREATE TABLE ... AS SELECT`: crear una tabla a partir del resultado de una consulta. (3) |
| **Dashboard** | Página con gráficos e indicadores que resume datos para tomar decisiones. (proyecto) |
| **Data lake (lago)** | Lugar donde se guardan archivos tal como llegan, barato y flexible. (3) |
| **Data warehouse (almacén)** | Base de datos optimizada para analizar grandes volúmenes con SQL, como BigQuery. (3) |
| **Dataset (BigQuery)** | "Carpeta" de tablas dentro de un proyecto. (3) |
| **DataFrame** | Tabla en memoria (pandas) o distribuida (Spark) que se manipula con código. (1, 6) |
| **Dimensión (`dim_`)** | Tabla que describe cosas: zonas, dispositivos, clientes. (4) |
| **Docker Compose** | Archivo y comando para levantar varios contenedores juntos. (1) |
| **Dry run** | Pedir a BigQuery que **estime** una consulta sin ejecutarla. (3) |
| **Emulador** | Programa que imita a otro, como LocalCloud imita a Google Cloud. (LocalCloud) |
| **Endpoint** | La dirección (URL) a la que un programa envía sus peticiones. (LocalCloud) |
| **ETL / ELT** | Extraer, transformar y cargar, o extraer, cargar y transformar. Cambia **dónde** se transforma. (2) |
| **Evento** | Registro de algo que pasó en un momento. (7) |
| **Hechos (`fct_`)** | Tabla con eventos medibles: viajes, ventas, latidos. (4) |
| **Heartbeat (latido)** | Mensaje periódico con el que un dispositivo dice "sigo vivo". (proyecto) |
| **Idempotente** | Que ejecutarlo varias veces da el mismo resultado que una sola vez. (2) |
| **Imagen (Docker)** | La "receta congelada" a partir de la cual se crean contenedores. (1) |
| **Incremental** | Cargar solo lo nuevo desde la última ejecución. (taller dlt) |
| **Ingesta** | Traer datos desde una fuente hacia tu sistema. (1, taller dlt) |
| **Linaje (lineage)** | El mapa de qué tabla se construye a partir de cuál. (4, 5) |
| **Materializar** | Guardar el resultado de una consulta como tabla real. (3, 4) |
| **Offset** | Posición de un mensaje dentro de una partición de un tópico. (7) |
| **OLAP / OLTP** | Sistemas para analizar o para registrar operaciones. (3) |
| **Orquestador** | Herramienta que coordina cuándo y en qué orden corren las tareas. (2) |
| **Parquet** | Formato de archivo por columnas y comprimido, ideal para análisis. (3) |
| **Particionamiento** | Dividir una tabla o archivo en partes (por ejemplo, por día) para leer solo lo necesario. (3, 6) |
| **Pipeline** | Secuencia de pasos que mueve y transforma datos. (todos) |
| **Poda de particiones** | Saltarse las particiones que no cumplen el filtro. (3) |
| **Productor / consumidor** | Programa que envía mensajes o programa que los lee. (7) |
| **Prueba de datos (test)** | Regla que verifica que los datos cumplen algo, como "no hay nulos". (4, 5) |
| **Seed** | CSV pequeño que se carga como tabla, normalmente un catálogo. (4, 5) |
| **Semilla (seed aleatoria)** | Número que hace que los datos "aleatorios" salgan siempre iguales. (todos los laboratorios) |
| **Shuffle** | Mover datos entre máquinas en Spark para agrupar o unir; es costoso. (6) |
| **SLO** | Objetivo de nivel de servicio, por ejemplo "99 % de disponibilidad". (proyecto) |
| **Staging** | Capa donde los datos crudos se limpian y estandarizan. (4, proyecto) |
| **Streaming** | Procesar los datos apenas llegan. (7) |
| **Tabla externa** | Tabla de BigQuery que lee archivos del bucket sin copiarlos. (3) |
| **Tópico** | Canal con nombre donde se publican mensajes de un tipo. (7) |
| **Trigger** | Lo que dispara un flujo automáticamente: un horario, un archivo nuevo, etc. (2) |
| **Upsert** | Insertar si no existe y actualizar si existe. (taller dlt, 7) |
| **Ventana (window)** | Agrupación de eventos por intervalo de tiempo: TUMBLE, HOP o SESSION. (7) |
| **Volumen (Docker)** | Disco que guarda datos aunque se borre el contenedor. (1) |
| **Watermark** | En streaming, la señal de "ya no espero eventos anteriores a esta hora". (7) |
| **YAML** | Formato de texto para configuraciones, basado en sangrías y `clave: valor`. (2) |
