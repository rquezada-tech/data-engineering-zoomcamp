# LocalCloud: Google Cloud en tu Mac

[← Antes de empezar](00-antes-de-empezar.md) · [Índice](../../README.md) · [Módulo 1 →](modulo-01-docker-postgres.md)

> **En una frase:** LocalCloud es un programa que se hace pasar por Google Cloud dentro de un contenedor Docker, para que practiques BigQuery y Cloud Storage sin cuenta ni costos.

---

## 1. ¿Qué es un emulador y por qué lo usamos?

Un **emulador** es un programa que **imita** a otro. Los emuladores de consolas de videojuegos imitan una consola dentro de tu computador. LocalCloud imita servicios de Google Cloud.

Las librerías oficiales de Google, como `google-cloud-bigquery`, envían peticiones a una **dirección**, también llamada *endpoint*. Normalmente es `https://bigquery.googleapis.com`. Si cambias esa dirección por `http://localhost:5388`, la misma librería habla con LocalCloud. Tu código es casi idéntico al que usarías en la nube real.

```text
             ¿a quién le hablo?
tu script ──────────────────────────► https://bigquery.googleapis.com  (Google real: cuenta y $$)
     │
     └──── api_endpoint=localhost ──► http://localhost:5388            (LocalCloud: gratis, en tu Mac)
```

**Ventajas:** es gratis, no pide cuenta, todo queda en tu Mac y puedes borrar todo y empezar de cero en segundos.

**Limitaciones:** es una **imitación**. Hay cosas que no reproduce fielmente: los costos, la velocidad a gran escala, los permisos de producción y las estimaciones de bytes. Cada guía lo advierte cuando importa.

## 2. Encender, comprobar y apagar

Todos los comandos se ejecutan desde la raíz del repositorio. La configuración está en [`laboratorios/localcloud/docker-compose.yml`](../../laboratorios/localcloud/docker-compose.yml).

**Encender.** La primera vez descarga la imagen, que ocupa unos 1,5 GB en disco:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

`-d` significa "en segundo plano" y `--wait` hace que Docker espere hasta que el servicio esté sano.

**Comprobar:**

```bash
curl -fsS http://localhost:5380/readiness && echo " <- LocalCloud listo"
```

**Consola web:** abre <http://localhost:5380/> en tu navegador.

**Ver los registros (logs)** si algo falla:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml logs --tail 50
```

**Apagar** conservando lo que creaste:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down
```

**Apagar y borrar todo** (buckets, tablas):

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down -v
```

## 3. Las direcciones que debes conocer

| Servicio | Dirección local | Variable de entorno |
|---|---|---|
| Gateway y consola | `http://localhost:5380` | `LOCALCLOUD_GATEWAY` |
| Cloud Storage | `http://localhost:5382` | `STORAGE_EMULATOR_HOST` |
| BigQuery (REST) | `http://localhost:5388` | `BIGQUERY_EMULATOR_HOST` |
| Proyecto | `local-gcp-project` | `GOOGLE_CLOUD_PROJECT` |

LocalCloud publica todas sus variables en un formato que la Terminal entiende. Para cargarlas en tu sesión:

```bash
eval "$(curl -fsS 'http://localhost:5380/env?format=shell')"
```

Los laboratorios de esta ruta **no necesitan** este paso: si las variables no existen, usan las direcciones de la tabla.

## 4. Cómo conectar tu propio código

```python
from google.auth.credentials import AnonymousCredentials
from google.cloud import bigquery, storage

PROYECTO = "local-gcp-project"
anonimo = AnonymousCredentials()  # LocalCloud no pide usuario ni clave

bq = bigquery.Client(project=PROYECTO, credentials=anonimo,
                     client_options={"api_endpoint": "http://localhost:5388"})
gcs = storage.Client(project=PROYECTO, credentials=anonimo,
                     client_options={"api_endpoint": "http://localhost:5382"})
```

### Protección contra conexiones accidentales a Google

El laboratorio del módulo 3 incluye [`lab/comun.py`](../../laboratorios/03-bigquery-parquet/lab/comun.py), que puedes reutilizar en tus propios proyectos. Antes de conectarse:

1. Revisa que todas las direcciones sean `localhost`, `127.0.0.1` o `::1`.
2. Bloquea cualquier conexión a `*.googleapis.com` y otros dominios de Google.
3. Revisa que LocalCloud responda. Si no responde, se detiene con un mensaje claro y **no** intenta usar la nube real.

## 5. Qué funciona y qué no (según nuestras pruebas)

Probado el 2026-11-17 en macOS con Apple Silicon y la imagen fijada en el compose:

| Función | ¿Funciona en LocalCloud? |
|---|---|
| Crear buckets, subir, listar y borrar objetos | ✅ Sí |
| Crear datasets | ✅ Sí |
| `CREATE EXTERNAL TABLE` sobre Parquet en el bucket | ✅ Sí |
| Consultas SQL (`GROUP BY`, `JOIN`, funciones de fecha) | ✅ Sí |
| `CREATE TABLE ... AS SELECT` (materializar) | ✅ Sí |
| `PARTITION BY DATE(...)` y `CLUSTER BY` | ✅ Sí: se crean las particiones y se registran los campos |
| `INFORMATION_SCHEMA.PARTITIONS` y `.TABLES` | ✅ Sí |
| *Dry run* (estimación de bytes) | ⚠️ Responde, pero **las cifras no equivalen a BigQuery real** (no simula la poda de particiones) |
| BigQuery ML | ❌ Requiere la imagen "full" del emulador (no probada) o GCP |
| Costos y facturación reales | ❌ Solo en GCP |
| Dataproc, Compute Engine, Cloud Run | ❌ Requieren dar acceso al socket de Docker; no se usan en esta ruta |

Documentación oficial: <https://local.cloud/docs/> · [BigQuery](https://local.cloud/services/bigquery/) · [Cloud Storage](https://local.cloud/services/cloud-storage/) · [Licencia](https://local.cloud/license/)

## 6. Sobre la licencia y la privacidad

LocalCloud **no es software libre**: tiene una licencia propietaria de "vista previa pública", gratuita para uso individual y proyectos de código abierto al momento de escribir esta guía. Revisa los términos vigentes en <https://local.cloud/license/>.

El emulador envía telemetría de uso por defecto. En nuestro `docker-compose.yml` la **desactivamos** con `LOCALCLOUD_TELEMETRY=false`.

## 7. Errores frecuentes

| Problema | Solución |
|---|---|
| `Cannot connect to the Docker daemon` | Abre Docker Desktop y espera a que termine de iniciar |
| `port is already allocated` | Otro programa usa los puertos 5380-5405. Revisa con `docker ps` y apaga lo que sobre |
| `curl: (52) Empty reply from server` justo después de encender | El emulador aún está iniciando: espera unos segundos o usa `--wait` |
| Se perdieron mis tablas | Usaste `down -v`, que borra el volumen de datos. Usa `down` sin `-v` para conservarlos |

[← Antes de empezar](00-antes-de-empezar.md) · [Índice](../../README.md) · [Módulo 1 →](modulo-01-docker-postgres.md)
