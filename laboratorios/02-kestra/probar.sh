#!/usr/bin/env bash
# Ejecuta cada flujo a través de la API, espera a que termine y revisa el resultado.
# Al final comprueba que la tabla public.lecturas tenga datos en la base datos_postgres.
# Uso (desde esta carpeta, después de ./cargar_flujos.sh):  ./probar.sh
set -euo pipefail
cd "$(dirname "$0")"

KESTRA_USUARIO="admin@kestra.io"
KESTRA_CLAVE="Admin1234!"
if [ -f .env ]; then
  # shellcheck disable=SC1091
  . ./.env
fi
KESTRA_URL="${KESTRA_URL:-http://localhost:8080}"
AUTH="${KESTRA_USUARIO}:${KESTRA_CLAVE}"
NS="dez.es.m2"
fallas=0

ejecutar() {   # ejecutar <flow_id> [campo=valor ...]
  local flujo="$1"; shift
  local campos=()
  for par in "$@"; do campos+=(-F "$par"); done
  local id
  # La API de ejecuciones recibe los inputs como formulario multipart.
  id=$(curl -fsS -u "$AUTH" -X POST "${campos[@]+"${campos[@]}"}" \
        "${KESTRA_URL}/api/v1/main/executions/${NS}/${flujo}" | sed -E 's/.*"id":"([^"]+)".*/\1/')
  local estado=""
  for _ in $(seq 1 60); do
    estado=$(curl -fsS -u "$AUTH" "${KESTRA_URL}/api/v1/main/executions/${id}" \
             | sed -E 's/.*"state":\{"current":"([A-Z_]+)".*/\1/')
    case "$estado" in SUCCESS|FAILED|KILLED|WARNING) break ;; esac
    sleep 2
  done
  if [ "$estado" = "SUCCESS" ]; then
    echo "  [OK]    ${flujo} $* -> ${estado} (ejecución ${id})"
  else
    echo "  [FALLA] ${flujo} $* -> ${estado} (ejecución ${id}). Revisa los logs en ${KESTRA_URL}/ui/main/executions/${NS}/${flujo}/${id}"
    fallas=$((fallas + 1))
  fi
}

echo "Ejecutando flujos..."
ejecutar hola_mundo nombre=Latinoamérica
ejecutar python_csv lecturas=50
ejecutar cargar_postgres fecha=2024-01-01
ejecutar cargar_postgres fecha=2024-01-02
ejecutar cargar_postgres fecha=2024-01-01   # re-ejecución: NO debe duplicar filas

echo
echo "Revisando la base datos_postgres..."
resultado=$(docker compose exec -T datos_postgres psql -U datos -d sensores -tA -c \
  "SELECT medido_en::date AS dia, COUNT(*) AS filas FROM public.lecturas GROUP BY 1 ORDER BY 1;" \
  | sed 's/|/ -> /')
echo "$resultado" | sed 's/^/  /'
total=$(docker compose exec -T datos_postgres psql -U datos -d sensores -tA -c "SELECT COUNT(*) FROM public.lecturas;")
if [ "$total" = "288" ]; then
  echo "  [OK]    public.lecturas tiene 288 filas (144 por día x 2 días, sin duplicados)"
else
  echo "  [FALLA] public.lecturas tiene ${total} filas; se esperaban 288"
  fallas=$((fallas + 1))
fi

echo
if [ "$fallas" -eq 0 ]; then
  echo "LABORATORIO KESTRA OK ✅"
else
  echo "${fallas} comprobación(es) fallaron."
  exit 1
fi
