# Laboratorio módulo 2 · Kestra en tu computador

> Adaptación no oficial en español del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) de DataTalks.Club. Los flujos de esta carpeta son originales.
> La explicación de los conceptos (qué es orquestar, flujos, tareas, triggers, backfill) está en la guía [`docs/es/modulo-02-kestra.md`](../../docs/es/modulo-02-kestra.md).

## Qué hace este laboratorio

Levanta **Kestra** (un orquestador de flujos de datos) junto a dos bases PostgreSQL, y ejecuta tres flujos escritos para este curso:

| Flujo | Qué hace |
|---|---|
| `hola_mundo` | Recibe un nombre y lo saluda en los logs. Sirve para conocer la interfaz. |
| `python_csv` | Ejecuta un script de Python que genera un CSV con lecturas de sensores **inventadas**. |
| `cargar_postgres` | Genera las lecturas de un día y las carga en PostgreSQL. Si lo repites, no duplica datos. Trae un trigger diario (desactivado) para practicar programación y *backfill*. |

No necesitas cuenta de Google Cloud ni conexión a internet, salvo para descargar las imágenes de Docker la primera vez.

## Requisitos

- Docker Desktop abierto (en Mac con Apple Silicon funciona tal cual).
- Unos 2 GB de RAM libres.
- Los puertos **8080** (Kestra) y **5434** (base de datos) libres.

## Paso a paso

Todos los comandos se ejecutan **dentro de esta carpeta** (`laboratorios/02-kestra`).

**1. Encender todo**

```bash
docker compose up -d
```

La primera vez descarga las imágenes (≈ 1 GB) y Kestra tarda entre 30 segundos y 2 minutos en quedar listo.

**2. Abrir la interfaz web**

Entra a <http://localhost:8080> con estas credenciales **de prueba**, que solo existen en tu computador:

- Usuario: `admin@kestra.io`
- Contraseña: `Admin1234!`

Si quieres cambiarlas, copia `.env.example` a `.env`, edítalo y vuelve a ejecutar `docker compose up -d`.

**3. Cargar los flujos**

```bash
./cargar_flujos.sh
```

Resultado esperado:

```text
  OK  dez.es.m2.hola_mundo  (flows/01_hola_mundo.yaml)
  OK  dez.es.m2.python_csv  (flows/02_python_csv.yaml)
  OK  dez.es.m2.cargar_postgres  (flows/03_cargar_postgres.yaml)
```

En la interfaz, menú **Flows**, verás los tres flujos en el namespace `dez.es.m2`. También puedes copiar y pegar el YAML a mano con el botón **Create**, y el resultado es el mismo.

**4. Ejecutar y comprobar**

```bash
./probar.sh
```

El script ejecuta cada flujo, espera a que termine y revisa la base de datos. Resultado esperado:

```text
  [OK]    hola_mundo nombre=Latinoamérica -> SUCCESS
  [OK]    python_csv lecturas=50 -> SUCCESS
  [OK]    cargar_postgres fecha=2024-01-01 -> SUCCESS
  [OK]    cargar_postgres fecha=2024-01-02 -> SUCCESS
  [OK]    cargar_postgres fecha=2024-01-01 -> SUCCESS
  2024-01-01 -> 144
  2024-01-02 -> 144
  [OK]    public.lecturas tiene 288 filas (144 por día x 2 días, sin duplicados)
LABORATORIO KESTRA OK ✅
```

Fíjate en que `2024-01-01` se ejecuta **dos veces** y aun así quedan 144 filas: el flujo borra el día antes de cargarlo.

En la interfaz, menú **Executions**, puedes abrir cada ejecución y ver el diagrama (pestaña *Gantt*), los logs y los archivos generados (pestaña *Outputs*).

**5. Mirar los datos con tus propios ojos (opcional)**

```bash
docker compose exec datos_postgres psql -U datos -d sensores -c "SELECT * FROM lecturas LIMIT 5;"
```

O conéctate con cualquier cliente SQL (DBeaver, pgAdmin, TablePlus) a `localhost:5434`, base `sensores`, usuario `datos`, contraseña `datos`.

## Apagar

```bash
docker compose down        # apaga todo y conserva los datos para la próxima vez
docker compose down -v     # apaga todo y BORRA los datos (vuelves a cero)
```

## Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `cargar_flujos.sh` dice "Kestra no respondió" | Espera un minuto más y reintenta. Revisa `docker compose logs kestra`. |
| `port is already allocated` al encender | Otro programa usa el 8080 o el 5434. Apágalo, o cambia el número de la izquierda en `ports:` del `docker-compose.yml`. |
| La interfaz pide usuario y contraseña y no entra | Usa exactamente `admin@kestra.io` / `Admin1234!` (o lo que pusiste en `.env`). |
| Un flujo queda en `FAILED` | Abre la ejecución en la interfaz → pestaña *Logs*: el error aparece en rojo en la tarea que falló. |

## Diferencias con el curso oficial

- El curso usa el *task runner* **Docker** para Python (crea un contenedor aparte por tarea). Aquí usamos **Process**: el script corre dentro del contenedor de Kestra, que ya trae Python 3. Así no hace falta montar el socket de Docker ni descargar más imágenes.
- No se descargan los datos de taxis de Nueva York: los datos son sintéticos y se generan con una semilla fija, así todos obtienen el mismo resultado.
- Los flujos de GCP del curso (subir a GCS y cargar a BigQuery) no están aquí. La versión local de BigQuery se trabaja en el [laboratorio del módulo 3](../03-bigquery-parquet/).
