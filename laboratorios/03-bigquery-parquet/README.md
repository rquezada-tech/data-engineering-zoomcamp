# Laboratorio 3 · De un Parquet a BigQuery, todo en tu Mac

> Parte de la [ruta en español](../../README.md) (adaptación no oficial). La explicación de conceptos está en la [guía del módulo 3](../../docs/es/modulo-03-data-warehouse-bigquery.md). Este archivo es la "receta" para ejecutar.

**Clasificación:** 🟡 *adaptado a local*. Usa BigQuery y Cloud Storage **emulados** con [LocalCloud](https://local.cloud/). No necesitas cuenta de Google ni tarjeta de crédito.

## Qué vas a hacer

```text
 tu Mac                                LocalCloud (contenedor Docker)
┌──────────────────────┐  sube   ┌─────────────────────────┐
│ 1. Genera 3 Parquet  │ ──────► │ 2. Bucket gs://dez-lab-m3│
│    con datos         │         └───────────┬─────────────┘
│    inventados        │                     │ lee (sin copiar)
└──────────────────────┘         ┌───────────▼─────────────┐
                                 │ 3. Tabla EXTERNA        │
                                 │ 4. Consultas SQL        │
                                 │ 5. Tabla INTERNA (copia)│
                                 │ 6. Tabla particionada   │
                                 │    y con clustering     │
                                 └─────────────────────────┘
```

## Requisitos

- Docker Desktop abierto.
- `uv` (gestor de Python). Revisa [Antes de empezar](../../docs/es/00-antes-de-empezar.md).

## Paso a paso

Todos los comandos se ejecutan desde la **raíz del repositorio**, salvo que se indique otra cosa.

**1. Enciende LocalCloud** (la primera vez descarga la imagen, unos minutos):

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

Comprueba que respondió:

```bash
curl -fsS http://localhost:5380/readiness && echo " <- LocalCloud listo"
```

**2. Entra a la carpeta del laboratorio e instala las librerías de Python:**

```bash
cd laboratorios/03-bigquery-parquet
```

```bash
uv sync
```

**3. Ejecuta el laboratorio completo:**

```bash
./ejecutar_lab.sh
```

O paso por paso, que es lo recomendado la primera vez para leer qué hace cada uno:

```bash
uv run python lab/00_verificar_entorno.py
uv run python lab/01_generar_parquet.py
uv run python lab/02_subir_a_bucket.py
uv run python lab/03_crear_tabla_externa.py
uv run python lab/04_consultar_tabla_externa.py
uv run python lab/05_materializar_tabla_interna.py
uv run python lab/06_particion_y_clustering.py
uv run python lab/07_comprobar.py
```

## Qué resultado esperar

Los datos se generan con una semilla fija, así que **tus números deben ser idénticos** a estos:

| Pregunta | Resultado |
|---|---|
| Viajes en la tabla externa | 6000 (2000 por mes: enero, febrero y marzo de 2024) |
| Zona con más viajes | Centro, con 1771 |
| Viajes con tarifa 0 | 60 |
| Filas en la tabla interna (sin tarifa 0) | 5940 |
| Suma de tarifas de la tabla interna | 77143.64 |
| Particiones diarias | 91 |
| Particiones que necesita la consulta de 1 semana | 7 de 91 (487 filas, 8,2 %) |

El último paso imprime:

```text
LABORATORIO OK ✅
```

## Cómo comprobarlo por tu cuenta

- `lab/07_comprobar.py` compara lo que hay en tus archivos Parquet con lo que responde BigQuery local. Si algo no cuadra, termina con código 1 y te dice qué falló.
- Abre la consola web de LocalCloud en <http://localhost:5380/> para mirar el bucket y las tablas con el navegador.

## Sobre los "bytes procesados"

El paso 6 pide a BigQuery una **estimación** de bytes (`dry_run`). Las cifras que ves salen del **emulador** y **no** equivalen a las de BigQuery real. Por ejemplo, el emulador no aplica la poda de particiones en la estimación. Usa este laboratorio para aprender *cómo* se pide la estimación y *cómo* se diseña una tabla particionada. Para comparar bytes reales, revisa el [apéndice opcional de GCP](../../docs/es/apendice-gcp.md).

## Seguridad: este laboratorio nunca habla con Google Cloud

`lab/comun.py` hace tres cosas antes de cada paso:

1. Solo acepta endpoints en `localhost`, `127.0.0.1` o `::1`. Si una variable como `BIGQUERY_EMULATOR_HOST` apunta a otro lugar, se detiene.
2. Bloquea a nivel de red cualquier nombre `*.googleapis.com` o `*.google.com`.
3. Revisa que LocalCloud esté encendido. Si no lo está, te dice cómo encenderlo y termina con código 2. **No** intenta usar Google Cloud real como alternativa.

Usa credenciales anónimas: no lee ninguna credencial de tu equipo.

## Repetir desde cero

```bash
uv run python lab/99_limpiar.py
rm -rf datos
./ejecutar_lab.sh
```

## Apagar

Desde la raíz del repositorio:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down        # apaga y conserva los datos
docker compose -f laboratorios/localcloud/docker-compose.yml down -v     # apaga y BORRA los datos del emulador
```

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `No pude hablar con LocalCloud` | El contenedor está apagado | Ejecuta el `docker compose ... up -d --wait` del paso 1 |
| `port is already allocated` al encender | Otro programa usa los puertos 5380-5405 | Apaga el otro programa o un LocalCloud anterior: `docker ps` |
| `mis-aligned LINKEDIT string pool` | Tu Python es x86_64 (Rosetta) | Lee [¿Tu Mac usa herramientas arm64?](../../docs/es/00-antes-de-empezar.md#42-tu-mac-usa-herramientas-arm64) |
| `uv: command not found` | Falta uv | `brew install uv` |
