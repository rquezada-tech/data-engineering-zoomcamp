# LocalCloud: tu "Google Cloud de bolsillo"

> Parte de la [ruta en español](../../README.es.md) (adaptación no oficial). Explicación completa en [docs/es/localcloud.md](../../docs/es/localcloud.md).

[LocalCloud](https://local.cloud/) es un programa que **imita** servicios de Google Cloud (BigQuery, Cloud Storage y otros) dentro de un contenedor Docker en tu computador. Las librerías oficiales de Google (por ejemplo `google-cloud-bigquery`) creen que hablan con Google, pero en realidad hablan con tu Mac.

## Encender

Desde la raíz del repositorio:

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait
```

## Comprobar

```bash
curl -fsS http://localhost:5380/readiness && echo " <- listo"
```

Consola web: <http://localhost:5380/>

## Cargar las variables de entorno (opcional)

Los laboratorios de esta ruta ya saben dónde está LocalCloud. Si quieres usar tus propios scripts o la CLI `gcloud`, carga las variables que publica el emulador:

```bash
eval "$(curl -fsS 'http://localhost:5380/env?format=shell')"
echo "$BIGQUERY_EMULATOR_HOST  $STORAGE_EMULATOR_HOST  $GOOGLE_CLOUD_PROJECT"
```

Deberías ver `http://localhost:5388  http://localhost:5382  local-gcp-project`.

## Apagar

```bash
docker compose -f laboratorios/localcloud/docker-compose.yml down       # conserva los datos
docker compose -f laboratorios/localcloud/docker-compose.yml down -v    # borra los datos
```

## Datos de esta configuración

| Dato | Valor |
|---|---|
| Imagen | `agentcloud/localcloud` fijada por digest `sha256:33622d53…219e` (publicada el 2026-11-10, arm64 y amd64) |
| Puertos | `127.0.0.1:5380-5405` (solo accesibles desde tu Mac) |
| BigQuery | `http://localhost:5388` |
| Cloud Storage | `http://localhost:5382` |
| Proyecto | `local-gcp-project` |
| Memoria | límite de 4 GB |
| Telemetría | desactivada (`LOCALCLOUD_TELEMETRY=false`) |
| Licencia | Propietaria, en vista previa pública y gratis para uso individual y de código abierto. Revisa <https://local.cloud/license/> |

Probado en macOS (Apple Silicon, arm64) con Docker 29.9.2 el 2026-11-17.
