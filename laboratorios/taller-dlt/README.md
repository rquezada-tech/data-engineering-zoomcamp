# Laboratorio · Taller de ingesta con `dlt`

> Parte de la [ruta en español](../../README.md). La guía con la explicación de los conceptos está en [docs/es/taller-dlt.md](../../docs/es/taller-dlt.md).

**Qué vas a hacer:** cargar pedidos de una tienda inventada a una base de datos DuckDB usando `dlt`, primero completos y después **solo los nuevos** (carga incremental).

**Qué necesitas:** `uv` instalado. No necesitas Docker, ni internet (aparte de instalar las librerías la primera vez), ni cuentas en la nube.

**Clasificación:** 🟢 local sin cambios (el taller oficial también usa DuckDB).

## Paso a paso

Todos los comandos se ejecutan dentro de esta carpeta:

```bash
cd laboratorios/taller-dlt
uv sync
```

### 1. Primera carga: "hoy existen 3 días de pedidos"

```bash
uv run python pipeline.py --dias 3
```

Deberías ver cómo `dlt` pide 8 páginas a la API falsa y, al final:

```text
Filas cargadas en ESTA ejecución:
  clientes: 40
  pedidos: 360
```

### 2. Pasaron dos días: "ahora existen 5 días de pedidos"

```bash
uv run python pipeline.py --dias 5
```

Resultado esperado: **solo 240 pedidos** (los de los días 4 y 5). `dlt` recordó la fecha del último pedido que cargó y se la pidió a la API como punto de partida.

```text
  clientes: 40
  pedidos: 240
```

### 3. Ejecuta lo mismo otra vez

```bash
uv run python pipeline.py --dias 5
```

Esta vez no aparece la línea `pedidos`, porque no hay pedidos nuevos. La tabla `clientes` se vuelve a cargar completa (40 filas) porque usa `write_disposition="replace"`.

### 4. Comprueba el resultado

```bash
uv run python consultar.py
```

Qué revisar:

| Pregunta | Resultado esperado |
|---|---|
| ¿Cuántos pedidos hay? | `600` (360 + 240) |
| ¿Rango de fechas? | de `2024-01-01 00:00` a `2024-01-05 23:48` (UTC) |
| ¿Duplicados? | `0` |
| ¿Qué pasó con el campo anidado `envio`? | se convirtió en dos columnas: `envio__ciudad` y `envio__express` |
| ¿Cuántas cargas hubo? | 3 filas en `_dlt_loads`, una por ejecución |

## Volver a empezar de cero

`dlt` guarda su "memoria" (el estado) en dos lugares: en la carpeta `.dlt_pipelines/` y dentro de la propia base de datos. Para reiniciar, borra ambos:

```bash
rm -rf tienda_local.duckdb .dlt_pipelines
```

Si borras solo uno, `dlt` recupera el estado desde el otro y seguirá cargando "solo lo nuevo".

## Problemas frecuentes

- **`Ambiguous reference to catalog or schema`**: pasa si el archivo DuckDB se llama igual que el dataset (por ejemplo `tienda.duckdb` con `dataset_name="tienda"`). Por eso aquí el archivo se llama `tienda_local.duckdb`.
- **`Pending packages are left in the pipeline`**: una carga anterior quedó a medias. Ejecuta `uv run dlt pipeline --pipelines-dir .dlt_pipelines tienda_local abort-packages` o reinicia como se explica arriba.
- **Las fechas aparecen con `-03:00` u otra zona horaria** al consultar DuckDB por tu cuenta: DuckDB las muestra en la zona horaria de tu Mac. `consultar.py` ejecuta `SET TimeZone = 'UTC'` para mostrarlas igual que en la fuente.

## Ejercicio propio

1. Agrega un campo `descuento` (entre 0 y 0.3) a cada pedido en `api_falsa_pedidos` y vuelve a ejecutar con `--dias 6`. ¿Qué hace `dlt` con la columna nueva en los pedidos antiguos?
2. Cambia `write_disposition` de `pedidos` a `"append"` y ejecuta dos veces seguidas con un número de días mayor. ¿Aparecen duplicados? ¿Por qué con `"merge"` no aparecían?
