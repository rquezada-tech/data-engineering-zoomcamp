"""Configuración del proyecto: nombres, fechas y umbrales en un solo lugar."""
from datetime import date
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = CARPETA_PROYECTO / "datos"
CARPETA_RAW = CARPETA_DATOS / "raw"
CATALOGO_CSV = CARPETA_PROYECTO / "seeds" / "catalogo_dispositivos.csv"

# Periodo simulado: 7 días completos (en UTC).
FECHA_INICIO = date(2026, 11, 1)
DIAS = 7

# Cada dispositivo envía un "latido" (heartbeat) cada 5 minutos -> 288 por día.
INTERVALO_MIN = 5
LATIDOS_POR_DIA = 24 * 60 // INTERVALO_MIN

# Lago de datos (Cloud Storage local) y warehouse (BigQuery local).
BUCKET = "telemetria-lago"
PREFIJO_RAW = "raw"
PREFIJO_SEEDS = "seeds"
DATASET = "telemetria"

TABLAS = {
    "catalogo": "dim_dispositivos",
    "raw": "raw_eventos_externa",
    "staging": "stg_eventos",
    "calidad": "calidad_resultados",
    "diaria": "disponibilidad_diaria",
    "resumen": "disponibilidad_dispositivo",
}

# Umbrales de calidad.
MAX_PCT_DESCARTADAS = 5.0          # si se descarta más del 5 % de las filas crudas, el pipeline se detiene
TEMPERATURA_VALIDA = (-40.0, 85.0)  # rango físico razonable para estos sensores
OBJETIVO_DISPONIBILIDAD = 99.0      # SLO: disponibilidad mínima esperada por dispositivo (%)
