# Antes de empezar

[Índice](../../README.md) · [LocalCloud →](localcloud.md)

> **En una frase:** aquí entiendes qué es la ingeniería de datos, cómo se recorre esta ruta y cómo dejar tu Mac listo.

**Tiempo estimado:** 45 a 60 minutos.

---

## 1. ¿Qué hace una persona ingeniera de datos?

Piensa en una ciudad. Las personas usan agua todos los días: abren la llave y sale limpia. Para que eso pase, alguien diseñó **cañerías** que llevan el agua desde ríos y pozos hasta una **planta** que la limpia, y desde ahí la reparten a las casas.

La ingeniería de datos hace lo mismo, pero con datos:

| Mundo del agua | Mundo de los datos | Lo verás en |
|---|---|---|
| Ríos y pozos | **Fuentes**: apps, sensores, APIs, archivos | Todos los módulos |
| Cañerías | **Pipelines**: programas que mueven datos | Módulos 1 y 2, taller dlt |
| Estanque de agua cruda | **Data lake**: archivos tal como llegan | Módulo 3 |
| Planta de tratamiento | **Transformaciones**: limpiar, unir, calcular | Módulos 4, 5 y 6 |
| Estanque de agua potable | **Data warehouse**: tablas listas para consultar | Módulo 3 |
| Horario de bombeo | **Orquestación**: qué corre, cuándo y en qué orden | Módulo 2 |
| Agua que corre sin parar | **Streaming**: datos que llegan en tiempo real | Módulo 7 |
| La llave de la cocina | **Dashboards** y reportes | Proyecto final |

Tu trabajo es que los datos lleguen **completos, correctos y a tiempo** a quienes los usan: analistas, científicos de datos o aplicaciones.

## 2. Cómo está organizada esta ruta

Esta ruta es una **adaptación no oficial, en español**, del [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) de [DataTalks.Club](https://datatalks.club/), cohorte 2026. Cambia dos cosas respecto del curso original:

1. **Idioma y nivel:** las guías están escritas para alguien que se está iniciando, con los conceptos explicados paso a paso.
2. **Todo corre en tu Mac:** donde el curso usa Google Cloud (GCP), aquí usamos [LocalCloud](localcloud.md), un emulador. No necesitas cuenta de Google ni tarjeta de crédito. Lo que **sí** requiere GCP de verdad está marcado y reunido en un [apéndice opcional](apendice-gcp.md).

Cada módulo tiene dos piezas:

- Una **guía** en `docs/es/`, que explica qué problema resuelve el módulo, los conceptos, qué vas a construir, cómo ejecutarlo, qué resultado esperar, cómo comprobarlo, un ejercicio original y los enlaces al material oficial.
- Un **laboratorio** en `laboratorios/`, con el código listo para ejecutar y un README con los pasos.

### La etiqueta de cada ejercicio

| Etiqueta | Significado |
|---|---|
| 🟢 **Local sin cambios** | Funciona igual que en el curso oficial, en tu Mac |
| 🟡 **Adaptado a local** | Funciona en tu Mac con LocalCloud o con otra herramienta local; puede haber diferencias con la nube real, y la guía las explica |
| 🔴 **Requiere GCP** | Para reproducirlo fielmente necesitas una cuenta de Google Cloud; está en el [apéndice opcional](apendice-gcp.md) |

La tabla completa está en [Clasificación de ejercicios](clasificacion-ejercicios.md).

### Cómo leer los comandos de las guías

- Los bloques que parten con ` ```bash ` son comandos para la **Terminal**. Cópialos **sin** el símbolo `$`; en esta ruta no lo ponemos.
- Si un comando dice `cd laboratorios/...`, se asume que partes desde la **raíz del repositorio**: la carpeta `data-engineering-zoomcamp`.
- Los nombres de comandos, librerías y funciones (`docker compose`, `SELECT`, `bigquery.Client`) se dejan en inglés, porque así los escribirás siempre.

## 3. Requisitos previos

No necesitas experiencia en datos. Sí ayuda:

- **Python básico:** variables, funciones, listas. Si nunca lo usaste, dedica unas horas a un tutorial introductorio.
- **SQL básico:** `SELECT`, `WHERE`, `GROUP BY`. El módulo 1 incluye un repaso.
- **Usar la Terminal:** abrir carpetas con `cd`, listar con `ls`. Más abajo hay una mini guía.

Hardware recomendado: Mac con Apple Silicon (M1 o superior), **16 GB de RAM** y unos **30 GB libres** en disco para imágenes de Docker. Con 8 GB funciona, pero conviene correr un laboratorio a la vez.

## 4. Instalar las herramientas

### 4.1 Homebrew: el instalador de programas

Homebrew instala programas de desarrollo con un solo comando. Si no lo tienes, sigue las instrucciones de <https://brew.sh>. Luego verifica:

```bash
brew --version
```

### 4.2 ¿Tu Mac usa herramientas arm64?

Los Mac con chip Apple (M1, M2, M3, M4…) usan la arquitectura **arm64**. Los Mac antiguos usaban **x86_64** (Intel). Un Mac con chip Apple puede ejecutar programas Intel gracias a **Rosetta**, pero a veces fallan librerías con partes compiladas.

Revisa tu situación:

```bash
uname -m
```

```bash
brew --prefix
```

```bash
file "$(which uv)" 2>/dev/null || echo "uv aún no está instalado"
```

| Resultado | Qué significa |
|---|---|
| `arm64`, `/opt/homebrew` y `uv: ... arm64` | Todo nativo: ideal ✅ |
| `arm64`, pero `/usr/local` o `uv: ... x86_64` | Tu Homebrew es el de Intel (quizás migraste desde un Mac antiguo). Funciona bajo Rosetta, pero algunas librerías pueden fallar |

**Caso real encontrado al probar esta ruta:** con un `uv` x86_64, la librería `cryptography` 50.x falló con el error `mis-aligned LINKEDIT string pool`. Con Python arm64 nativo funcionó sin problemas. Si te pasa:

- **Solución rápida** (ya aplicada en los laboratorios): limitar a `cryptography<49`.
- **Solución de fondo:** instalar Homebrew nativo en `/opt/homebrew` siguiendo <https://brew.sh> y reinstalar `uv` con ese Homebrew. También puedes pedirle a uv un Python arm64 explícitamente:

```bash
uv python install cpython-3.12-macos-aarch64-none
```

### 4.3 Docker Desktop

Docker permite ejecutar programas dentro de "**contenedores**": cajas aisladas que traen todo lo que el programa necesita. Así no tienes que instalar PostgreSQL, Kestra o Spark directamente en tu Mac. El [módulo 1](modulo-01-docker-postgres.md) lo explica en detalle.

1. Descarga Docker Desktop para **Mac con chip Apple** desde <https://www.docker.com/products/docker-desktop/>.
2. Ábrelo y espera a que el ícono de la ballena diga que está corriendo.
3. En *Settings → Resources*, asigna al menos **6 GB de memoria**, u **8 GB** para el módulo 7.

Verifica:

```bash
docker version --format '{{.Server.Version}} {{.Server.Arch}}'
```

```bash
docker compose version
```

Deberías ver algo como `29.x arm64` y `Docker Compose version v2.x` o superior.

### 4.4 uv: Python sin dolores de cabeza

[uv](https://docs.astral.sh/uv/) instala Python y las librerías de cada proyecto en un **entorno virtual**: una carpeta `.venv` propia de cada laboratorio. Así un laboratorio no rompe a otro.

```bash
brew install uv
```

```bash
uv --version
```

Dentro de cada laboratorio usarás siempre dos comandos:

- `uv sync`: instala exactamente las versiones indicadas en `uv.lock`.
- `uv run python archivo.py`: ejecuta el script con ese entorno.

### 4.5 Git y tu copia del repositorio

```bash
brew install git
```

```bash
git clone https://github.com/rquezada-tech/data-engineering-zoomcamp.git
```

```bash
cd data-engineering-zoomcamp && git switch adaptacion-es-localcloud
```

### 4.6 Un editor de código

Cualquiera sirve. Visual Studio Code es gratuito y muy usado. Te servirá para leer los scripts de los laboratorios, que vienen comentados en español.

## 5. Mini guía de Terminal

| Comando | Para qué sirve | Ejemplo |
|---|---|---|
| `pwd` | Muestra en qué carpeta estás | `pwd` |
| `ls` | Lista los archivos de la carpeta | `ls laboratorios` |
| `cd` | Entra a una carpeta (`cd ..` sube una) | `cd laboratorios/01-docker-postgres` |
| `cat` | Muestra el contenido de un archivo | `cat README.md` |
| `Ctrl + C` | Detiene el programa que está corriendo | — |
| `↑` | Repite el comando anterior | — |

## 6. Comprobación final

Si estos comandos responden sin error, estás listo:

```bash
docker run --rm hello-world | head -3
```

```bash
uv run --no-project python -c "import platform; print('Python OK en', platform.machine())"
```

Luego enciende LocalCloud y corre tu primer laboratorio de nube local, siguiendo la [guía de LocalCloud](localcloud.md).

## 7. Consejos para aprender mejor

- **No copies y pegues a ciegas.** Antes de ejecutar, lee qué hace el comando. Después, mira el resultado y compáralo con el "resultado esperado" de la guía.
- **Rompe cosas a propósito.** Cambia un número, apaga un contenedor y mira qué error aparece. Así aprendes a diagnosticar.
- **Toma notas** de los errores que resolviste. Compartir lo aprendido es parte del curso oficial (*learning in public*).
- **Avanza a tu ritmo.** El curso oficial dura unas 10 semanas; aquí no hay plazos.

[Índice](../../README.md) · [LocalCloud →](localcloud.md)
