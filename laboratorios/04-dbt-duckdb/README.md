# Laboratorio · Módulo 4: dbt con DuckDB

> Parte de la [ruta en español](../../README.es.md). La guía con los conceptos está en [docs/es/modulo-04-dbt-duckdb.md](../../docs/es/modulo-04-dbt-duckdb.md).

**Qué vas a construir:** un proyecto dbt llamado `viajes_locales` que toma viajes en bruto (archivos Parquet) y los transforma, capa por capa, hasta llegar a un reporte de ingresos mensuales por zona. Todo queda en un archivo DuckDB dentro de esta carpeta.

**Qué necesitas:** `uv`. No necesitas Docker ni nube.

**Clasificación:** 🟡 adaptado a local. El curso oficial ofrece dos caminos (BigQuery + dbt Cloud, o DuckDB + dbt Core). Aquí usamos DuckDB + dbt Core con un proyecto propio y datos sintéticos.

```text
datos/*.parquet ──► stg_viajes (vista) ──► int_viajes_validos ──► fct_viajes ──► ingresos_mensuales_por_zona
                                                              ▲
seeds: zonas.csv, tipos_pago.csv ──► dim_zonas ───────────────┘
```

## Paso a paso

```bash
cd laboratorios/04-dbt-duckdb
uv sync                              # instala dbt-core y dbt-duckdb
uv run python generar_datos.py       # crea datos/viajes_2024-01..03.parquet (6.000 viajes)
uv run dbt debug --profiles-dir .    # comprueba que dbt encuentra el perfil y DuckDB
uv run dbt build --profiles-dir .    # carga seeds, crea modelos y ejecuta pruebas
```

`--profiles-dir .` le dice a dbt que use el `profiles.yml` de esta carpeta (por defecto lo buscaría en `~/.dbt/`). Si no quieres escribirlo cada vez: `export DBT_PROFILES_DIR=.`

### Resultado esperado de `dbt build`

```text
Finished running 2 seeds, 4 table models, 17 data tests, 1 view model ...
Completed successfully
Done. PASS=24 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=24
```

### Comprobar

```bash
uv run python consultar.py
```

| Capa | Filas esperadas | Por qué |
|---|---|---|
| `staging.stg_viajes` | 6000 | todos los viajes, sin filtrar |
| `intermediate.int_viajes_validos` | 5936 | se quitan los 64 viajes con tarifa 0 |
| `marts.fct_viajes` | 5936 | uno por viaje válido |
| `marts.ingresos_mensuales_por_zona` | 24 | 3 meses × 8 zonas |

Top de enero 2024: `Centro` con 563 viajes y 7755.80 de ingresos, luego `Oriente` (4145.61) y `Norte` (3460.32).

### Ver la documentación y el linaje

```bash
uv run dbt docs generate --profiles-dir .
uv run dbt docs serve --profiles-dir . --port 8090
```

Abre http://localhost:8090 y haz clic en el ícono de grafo (abajo a la derecha) para ver el linaje. Detén el servidor con `Ctrl + C`.

### Comandos útiles para practicar

```bash
uv run dbt run --profiles-dir . --select stg_viajes        # solo un modelo
uv run dbt run --profiles-dir . --select +fct_viajes       # fct_viajes y todo lo que necesita antes
uv run dbt test --profiles-dir . --select fct_viajes       # solo las pruebas de un modelo
uv run dbt compile --profiles-dir . --select stg_viajes    # ver el SQL final (en target/compiled/)
```

## Volver a empezar

```bash
rm -f viajes_locales.duckdb && rm -rf target
uv run dbt build --profiles-dir .
```

## Problemas frecuentes

- **`Could not find profile named 'viajes_locales'`**: olvidaste `--profiles-dir .` o no estás dentro de esta carpeta.
- **`No files found that match the pattern "datos/viajes_*.parquet"`**: falta ejecutar `uv run python generar_datos.py`, o ejecutaste dbt desde otra carpeta (la ruta es relativa a donde corres el comando).
- **`Could not set lock on file ... viajes_locales.duckdb`**: otro programa (por ejemplo DBeaver o un `duckdb` abierto) tiene el archivo abierto. Ciérralo y vuelve a intentar. DuckDB permite un solo proceso escribiendo a la vez.
- **Los totales por mes no coinciden con los de esta guía**: revisa que `profiles.yml` tenga `TimeZone: UTC`. Sin eso, DuckDB usa la zona horaria de tu Mac y algunos viajes cambian de mes.
- **Mensaje "dbt v2 is available"**: es solo un aviso. Este laboratorio usa dbt Core 1.x, igual que el curso.

## Ejercicio propio

1. Crea `models/marts/reporting/viajes_por_tipo_pago.sql` que muestre, por mes, cuántos viajes y qué porcentaje del total se pagó con cada medio.
2. Agrégale pruebas `not_null` a `mes` y `tipo_pago`, y una prueba singular que verifique que los porcentajes de cada mes suman 100 (con un margen de 0.1).
3. Ejecuta `uv run dbt build --profiles-dir . --select +viajes_por_tipo_pago` y confirma que todo pasa.
