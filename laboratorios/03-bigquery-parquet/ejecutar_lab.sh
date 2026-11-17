#!/usr/bin/env bash
# Ejecuta el laboratorio completo, de principio a fin, en orden.
# Uso (desde esta carpeta):  ./ejecutar_lab.sh
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "Falta 'uv'. Instálalo con: brew install uv" >&2
  exit 2
fi

uv sync --quiet
for paso in 00_verificar_entorno 01_generar_parquet 02_subir_a_bucket 03_crear_tabla_externa \
            04_consultar_tabla_externa 05_materializar_tabla_interna 06_particion_y_clustering 07_comprobar; do
  uv run --quiet python "lab/${paso}.py"
done
