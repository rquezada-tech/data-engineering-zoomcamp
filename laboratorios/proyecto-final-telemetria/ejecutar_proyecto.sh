#!/usr/bin/env bash
# Corre el proyecto final completo: pruebas rápidas + pipeline. Luego abre el dashboard tú mismo.
# Uso (desde esta carpeta):  ./ejecutar_proyecto.sh
set -euo pipefail
cd "$(dirname "$0")"
command -v uv >/dev/null || { echo "Falta 'uv'. Instálalo con: brew install uv" >&2; exit 2; }
uv sync --quiet --group dev
uv run python -m telemetria.pipeline
uv run --group dev pytest -q
echo
echo "Para ver el dashboard:  uv run streamlit run dashboard/app.py"
