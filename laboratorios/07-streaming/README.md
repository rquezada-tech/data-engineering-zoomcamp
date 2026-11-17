# Laboratorio módulo 7 · Streaming con Redpanda, PyFlink y PostgreSQL

> Parte de la [ruta en español](../../README.es.md) (adaptación no oficial del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) de DataTalks.Club; código original de esta adaptación). Conceptos en la [guía del módulo 7](../../docs/es/modulo-07-streaming.md).

## Qué vas a construir

```text
productor.py ──► Redpanda (tópico "lecturas-sensores") ──► Flink: ventanas de 1 minuto ──► PostgreSQL
  (tu Mac)              (contenedor)                          (contenedores)                (contenedor)
```

- **Productor**: un script de Python que inventa lecturas de temperatura de 5 sensores (una cada 5 segundos de "tiempo de evento", durante 10 minutos).
- **Redpanda**: guarda los mensajes en orden. Es compatible con Kafka, así que se usa con las mismas herramientas.
- **Flink (PyFlink)**: lee el tópico de forma continua, agrupa las lecturas en ventanas de 1 minuto por sensor y calcula cantidad, promedio y máximo.
- **PostgreSQL**: recibe el resultado en la tabla `lecturas_por_minuto`.

## Requisitos

- Docker Desktop con **al menos 6 GB de RAM** asignados (Settings → Resources).
- [`uv`](https://docs.astral.sh/uv/) para ejecutar los scripts de Python de tu Mac.
- Puertos libres: `9092` (Redpanda), `8081` (Flink UI), `5433` (PostgreSQL) y `8082` (consola opcional).

## Paso a paso

Todos los comandos se ejecutan **desde esta carpeta** (`laboratorios/07-streaming`).

**1. Construir la imagen de Flink y encender todo.** La primera vez tarda entre 3 y 6 minutos porque instala PyFlink y descarga los conectores.

```bash
docker compose up -d --build --wait
```

Al final debes ver `Healthy` o `Started` en los cuatro contenedores (`redpanda`, `postgres`, `jobmanager`, `taskmanager`).

**2. Crear el tópico** (la "carpeta" donde se guardan los mensajes):

```bash
docker compose exec redpanda rpk topic create lecturas-sensores --partitions 1
```

**3. Instalar las librerías de Python del lado de tu Mac:**

```bash
uv sync
```

**4. Enviar los eventos:**

```bash
uv run python scripts/productor.py
```

Resultado esperado:

```text
Enviados 600 eventos + 1 de cierre al tópico 'lecturas-sensores' en 0.37 s
```

**5. Mirar algunos mensajes** (opcional, pero recomendado):

```bash
uv run python scripts/consumidor.py --cantidad 3
```

```text
particion=0 offset=0 valor={'sensor_id': 'sensor-01', 'temperatura': 19.49, 'ts': 1704110400000}
...
Mensajes leídos: 601. Lecturas con temperatura > 23 °C: 36
```

**6. Enviar el trabajo de Flink al clúster:**

```bash
docker compose exec jobmanager ./bin/flink run -py /opt/jobs/ventanas_por_minuto.py -d
```

Verás algunas líneas `WARNING: Unknown module: jdk.compiler` (son normales) y al final:

```text
Job has been submitted with JobID ...
```

Abre <http://localhost:8081>: en **Running Jobs** aparece el trabajo en estado `RUNNING`.

**7. Esperar unos 20 segundos y revisar PostgreSQL:**

```bash
uv run python scripts/consultar_postgres.py
```

Resultado esperado:

```text
Filas: 50 | ventanas de 1 minuto: 10 | sensores: 5
(datetime.datetime(2024, 1, 1, 12, 0), 'sensor-01', 12, Decimal('20.45'), 22.61)
(datetime.datetime(2024, 1, 1, 12, 0), 'sensor-02', 12, Decimal('19.64'), 22.88)
...
```

10 ventanas × 5 sensores = 50 filas, y cada fila resume **12 lecturas** (una cada 5 s durante 1 minuto).

También puedes consultar directamente con `psql` dentro del contenedor:

```bash
docker compose exec postgres psql -U postgres -d streaming -c "SELECT * FROM lecturas_por_minuto ORDER BY 1, 3 LIMIT 5;"
```

## ¿Por qué hace falta el "evento de cierre"?

Flink no sabe cuándo terminó un minuto mirando el reloj de tu computador: lo sabe mirando las horas **dentro de los eventos**.
La *marca de agua* (`WATERMARK`) dice "ya vi eventos hasta las 12:09:55, así que no espero nada anterior a 12:09:50".
Una ventana se cierra (y se escribe en PostgreSQL) solo cuando la marca de agua pasa su hora de término.
El productor envía al final un evento con hora 12:12 para empujar la marca de agua y cerrar la última ventana (12:09–12:10).
Pruébalo: borra todo (`docker compose down -v`), repite los pasos y en el paso 4 usa
`uv run python scripts/productor.py --sin-cierre`. Verás **45** filas en vez de 50: la última ventana nunca se cierra.

## Experimentos sugeridos

- Ejecuta el productor **otra vez**. ¿Cambia el conteo en PostgreSQL? (Pista: los eventos repetidos llegan "tarde" respecto de la marca de agua.)
- Abre la consola web de Redpanda para ver los mensajes:

  ```bash
  docker compose --profile consola up -d
  ```

  y entra a <http://localhost:8082>.

## Detener y limpiar

Detener sin borrar datos:

```bash
docker compose stop
```

Apagar y borrar todo (tópicos, tablas y contenedores):

```bash
docker compose --profile consola down -v
```

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `KafkaTimeoutError: Unable to bootstrap from 127.0.0.1:9092` | Redpanda no está encendido | `docker compose ps` y, si hace falta, `docker compose up -d --wait`. |
| `Failed to update metadata` usando `localhost:9092` | En macOS `localhost` puede ir por IPv6 | Usa `127.0.0.1:9092` (es el valor por defecto de los scripts). |
| La construcción falla en `pip install apache-flink` | Sin internet o poca memoria | Reintenta `docker compose build`; asigna más RAM a Docker. |
| PostgreSQL muestra 0 filas | El trabajo no está corriendo o no hay eventos | Revisa <http://localhost:8081> y los registros: `docker compose logs taskmanager`. |
| `port is already allocated` | Otro servicio usa 9092, 8081 o 5433 | Detén el otro servicio o cambia el puerto de la izquierda en `docker-compose.yml`. |

## Créditos

La forma de instalar PyFlink en arm64 (JDK completo + herramientas de compilación para `pemja`) y las versiones de los conectores
siguen lo que usa el módulo 7 del curso original (cohorte 2026). El código de este laboratorio es original.
