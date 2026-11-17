# Laboratorio 1 · Docker, PostgreSQL y una ingesta en contenedor

> Parte de la [ruta en español](../../README.es.md) (adaptación no oficial). Conceptos en la [guía del módulo 1](../../docs/es/modulo-01-docker-postgres.md).

**Clasificación:** 🟢 *local sin cambios* (no usa Google Cloud).

## Qué hace

1. Levanta **PostgreSQL 18** y **pgAdmin** con Docker Compose.
2. Construye una imagen de Docker con un script de Python (`ingesta/`).
3. El script genera 3600 lecturas **inventadas** de 5 estaciones meteorológicas (30 días, una por hora) y las carga en la tabla `lecturas` en trozos de 1000 filas.
4. Ejecutas consultas SQL de ejemplo (`consultas.sql`).

## Paso a paso

```bash
cd laboratorios/01-docker-postgres
```

**1. Encender la base de datos y pgAdmin:**

```bash
docker compose up -d --wait
```

**2. Construir y ejecutar la ingesta.** La primera vez descarga la imagen de Python e instala las librerías:

```bash
docker compose run --rm --build ingesta
```

Resultado esperado:

```text
CSV generado: 3600 filas
  trozo 1: 1000 filas cargadas
  trozo 2: 1000 filas cargadas
  trozo 3: 1000 filas cargadas
  trozo 4: 600 filas cargadas
Listo: la tabla 'lecturas' tiene 3600 filas
```

**3. Consultar:**

```bash
docker compose exec -T postgres psql -U estudiante -d clima < consultas.sql
```

Debes ver 720 lecturas por estación. La zona más calurosa es **Desierto**, con un promedio de 26,7 °C. El día con más lluvia es el **2025-11-18**, con 10,2 mm.

**4. Explorar con pgAdmin** en <http://localhost:8085>. Tarda unos 20 segundos en estar disponible.

- No pide clave al entrar, porque está en modo escritorio.
- Agrega un servidor con *Register → Server*. En la pestaña *Connection* usa:
  - **Host:** `postgres`. Es el nombre del servicio dentro de la red de Docker, no `localhost`.
  - **Puerto:** `5432`.
  - **Usuario y clave:** `estudiante` / `estudiante`.

**5. Conectarte desde tu Mac** con cualquier cliente SQL: host `localhost`, puerto `5432`, base `clima` y usuario/clave `estudiante`.

## Apagar

```bash
docker compose down      # conserva los datos en el volumen pg-datos
docker compose down -v   # borra también los datos
```

## Credenciales

Todas las claves de este laboratorio (`estudiante`) son **solo para practicar en tu computador**. Los puertos se publican únicamente en `127.0.0.1`, así que nadie fuera de tu Mac puede conectarse.

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `port 5432 is already allocated` | Tienes otro PostgreSQL encendido. Apágalo o cambia `"127.0.0.1:5432:5432"` por `"127.0.0.1:5442:5432"` |
| pgAdmin no carga | Espera unos 20 segundos o revisa `docker compose logs pgadmin` |
| `connection refused` desde pgAdmin | Usaste `localhost` como host. Dentro de Docker es `postgres` |

Probado el 2026-11-17 en macOS con Apple Silicon y Docker 29.9.2: imágenes `postgres:18` (PostgreSQL 18.7), `dpage/pgadmin4:9` y `python:3.13-slim`.
