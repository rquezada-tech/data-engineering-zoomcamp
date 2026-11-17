# Laboratorio · Módulo 5: plataforma de datos con Bruin

> Parte de la [ruta en español](../../README.md). La guía con los conceptos está en [docs/es/modulo-05-bruin.md](../../docs/es/modulo-05-bruin.md).

**Qué vas a construir:** un pipeline de Bruin llamado `invernadero` que genera lecturas de sensores de temperatura y humedad, las limpia, revisa su calidad automáticamente y produce un resumen diario con alertas de calor. Todo en un archivo DuckDB local.

**Qué necesitas:** la CLI de Bruin. No necesitas Docker, nube ni cuenta en Bruin Cloud. La primera ejecución necesita internet porque Bruin descarga Python, `pandas` y el driver de DuckDB.

**Clasificación:** 🟢 local sin cambios. El módulo oficial también usa DuckDB. Bruin Cloud es opcional.

```text
ingesta.invernaderos (CSV) ─┐
                            ├──► staging.lecturas_limpias ──► reportes.resumen_diario
ingesta.lecturas (Python) ──┘        (+ 9 controles)              (+ 2 controles)
```

## 1. Instalar Bruin

Método oficial ([documentación](https://getbruin.com/docs/bruin/getting-started/introduction/installation.html)):

```bash
curl -LsSf https://getbruin.com/install/cli | sh
```

> El script instala el programa en `~/.local/bin` y **agrega una línea a tu `~/.zshrc`** para que la terminal lo encuentre. Abre una terminal nueva después de instalar.

Si prefieres no modificar tu `~/.zshrc`, descarga el binario de la [página de releases](https://github.com/bruin-data/bruin/releases) y verifica su checksum. Necesitas `gh` con sesión iniciada; si no lo tienes, usa el método oficial.

```bash
mkdir -p /tmp/bruin && cd /tmp/bruin
gh release download -R bruin-data/bruin -p 'bruin_Darwin_arm64.tar.gz' -p '*checksums.txt'
grep bruin_Darwin_arm64.tar.gz *checksums.txt | shasum -a 256 -c -   # debe decir: OK
tar -xzf bruin_Darwin_arm64.tar.gz && install -m 0755 bruin ~/.local/bin/bruin
cd -
```

Comprueba la instalación:

```bash
bruin --version     # probado con v0.11.827
```

## 2. Ejecutar el pipeline

Desde esta carpeta:

```bash
cd laboratorios/05-bruin
bruin validate --config-file .bruin.yml invernadero
bruin run --config-file .bruin.yml --start-date 2024-03-01 --end-date 2024-03-07 invernadero
```

`--config-file .bruin.yml` es necesario porque Bruin, por defecto, busca ese archivo en la raíz del repositorio git, y este laboratorio vive en una subcarpeta.

> ⚠️ Si ejecutas un comando de Bruin **sin** `--config-file`, Bruin crea un `.bruin.yml` vacío en la raíz del repositorio y agrega líneas al `.gitignore` de la raíz. Para no tener que escribir la opción en cada comando, ejecuta esto una vez en la terminal:
>
> ```bash
> export BRUIN_CONFIG_FILE="$PWD/.bruin.yml"
> ```
>
> La variable dura mientras la terminal esté abierta.

Resultado esperado. La primera vez tarda entre 20 y 60 segundos, porque Bruin prepara el entorno de Python:

```text
PASS ingesta.invernaderos ...
PASS ingesta.lecturas
PASS staging.lecturas_limpias ........
PASS reportes.resumen_diario ..

 ✓ Assets executed      4 succeeded
 ✓ Quality checks       13 succeeded
```

## 3. Comprobar

```bash
bruin query --config-file .bruin.yml --connection duckdb-local --query "
SELECT (SELECT COUNT(*) FROM ingesta.lecturas)          AS crudas,
       (SELECT COUNT(*) FROM staging.lecturas_limpias)  AS limpias,
       (SELECT COUNT(*) FROM reportes.resumen_diario)   AS filas_reporte,
       (SELECT SUM(alertas_calor) FROM reportes.resumen_diario) AS alertas"
```

| Columna | Valor esperado | Por qué |
|---|---|---|
| `crudas` | 4032 | 7 días × 24 h × 4 lecturas/h × 6 sensores |
| `limpias` | 3931 | se descartan 101 lecturas sin temperatura |
| `filas_reporte` | 21 | 7 días × 3 invernaderos |
| `alertas` | 318 | lecturas sobre 30 °C (el umbral por defecto) |

## 4. Linaje y variables

Ver de qué depende un asset y qué depende de él:

```bash
BRUIN_CONFIG_FILE="$PWD/.bruin.yml" bruin lineage --full invernadero/assets/staging/lecturas_limpias.sql
```

(`bruin lineage` no tiene la opción `--config-file`, por eso aquí se usa la variable.)

Cambiar el umbral de alerta **sin editar el código**, ejecutando solo el reporte:

```bash
bruin run --config-file .bruin.yml --var umbral_temperatura_c=28 invernadero/assets/reportes/resumen_diario.sql
```

Si vuelves a ejecutar la consulta del paso 3, `alertas` ahora vale **641**, porque bajó el umbral.

## Volver a empezar

```bash
rm -f invernadero.duckdb
```

## Problemas frecuentes

- **Apareció un `.bruin.yml` en la raíz del repositorio y cambios en el `.gitignore` de la raíz**: ejecutaste Bruin sin `--config-file`. Desde la raíz del repositorio, deshazlo con `rm .bruin.yml && git checkout -- .gitignore`.
- **`bruin: command not found`**: abre una terminal nueva o revisa que `~/.local/bin` esté en tu `PATH` (`echo $PATH`).
- **Error de conexión `duckdb-local` no encontrada**: olvidaste `--config-file .bruin.yml` (o la variable `BRUIN_CONFIG_FILE`), o no estás en esta carpeta.
- **`Could not set lock on file invernadero.duckdb`**: otro programa tiene abierta la base. Ciérralo; DuckDB permite un solo proceso escribiendo a la vez.
- **La fecha aparece como `2024-03-01T00:00:00Z`** en `bruin query`: es solo el formato de salida de la consulta; la columna `fecha` es de tipo `date`.

## Ejercicio propio

1. Agrega al CSV un cuarto invernadero (`INV-4`, cultivo `pimiento`) y súmalo al diccionario `INVERNADEROS` de `lecturas.py`. Ejecuta el pipeline. ¿Qué control de calidad falla y por qué? Corrígelo.
2. Crea un asset `reportes/alertas_por_cultivo.sql` que cuente las alertas por cultivo para toda la semana. Ejecútalo con `bruin run` y revisa con `bruin lineage` que dependa de `staging.lecturas_limpias`.
