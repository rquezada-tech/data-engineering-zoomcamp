#!/usr/bin/env bash
# Sube (o actualiza) los flujos de la carpeta flows/ a Kestra usando su API.
# Uso (desde esta carpeta, con Kestra encendido):  ./cargar_flujos.sh
set -euo pipefail
cd "$(dirname "$0")"

# Credenciales de prueba (las mismas del docker-compose.yml). Un .env las puede cambiar.
KESTRA_USUARIO="admin@kestra.io"
KESTRA_CLAVE="Admin1234!"
if [ -f .env ]; then
  # shellcheck disable=SC1091
  . ./.env
fi
KESTRA_URL="${KESTRA_URL:-http://localhost:8080}"
AUTH="${KESTRA_USUARIO}:${KESTRA_CLAVE}"

echo "Esperando a que Kestra responda en ${KESTRA_URL} (la primera vez puede tardar 1-2 minutos)..."
for _ in $(seq 1 60); do
  if curl -fsS -u "$AUTH" "${KESTRA_URL}/api/v1/main/flows/search?size=1" >/dev/null 2>&1; then
    break
  fi
  sleep 5
done
if ! curl -fsS -u "$AUTH" "${KESTRA_URL}/api/v1/main/flows/search?size=1" >/dev/null 2>&1; then
  echo "Kestra no respondió. Revisa: docker compose ps   y   docker compose logs kestra" >&2
  exit 2
fi

for archivo in flows/*.yaml; do
  id=$(awk '/^id:/{print $2; exit}' "$archivo")
  ns=$(awk '/^namespace:/{print $2; exit}' "$archivo")
  # ¿Ya existe? Entonces lo actualizamos (PUT); si no, lo creamos (POST).
  existe=$(curl -sS -o /dev/null -w '%{http_code}' -u "$AUTH" "${KESTRA_URL}/api/v1/main/flows/${ns}/${id}")
  if [ "$existe" = "200" ]; then
    metodo=PUT; url="${KESTRA_URL}/api/v1/main/flows/${ns}/${id}"
  else
    metodo=POST; url="${KESTRA_URL}/api/v1/main/flows"
  fi
  codigo=$(curl -sS -o /tmp/kestra_respuesta.json -w '%{http_code}' -u "$AUTH" -X "$metodo" \
    -H "Content-Type: application/x-yaml" --data-binary @"$archivo" "$url")
  if [ "$codigo" = "200" ]; then
    echo "  OK  ${ns}.${id}  (${archivo})"
  else
    echo "  ERROR ${codigo} al subir ${archivo}:" >&2
    cat /tmp/kestra_respuesta.json >&2; echo >&2
    exit 1
  fi
done
echo "Flujos cargados. Míralos en ${KESTRA_URL}/ui/main/flows"
