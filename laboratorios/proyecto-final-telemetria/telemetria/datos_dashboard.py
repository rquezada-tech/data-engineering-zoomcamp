"""Consultas que alimentan el dashboard. Separadas de la interfaz para poder probarlas sin abrir el navegador.

Prueba rápida:
    uv run python -m telemetria.datos_dashboard
"""
import pandas as pd

from . import config
from .conexion import clientes


def _df(bq, consulta: str) -> pd.DataFrame:
    filas = [dict(f.items()) for f in bq.query(consulta).result()]
    return pd.DataFrame(filas)


def cargar() -> dict[str, pd.DataFrame]:
    bq, _ = clientes()
    base = f"`{bq.project}.{config.DATASET}"
    return {
        "resumen": _df(bq, f"SELECT * FROM {base}.{config.TABLAS['resumen']}` ORDER BY disponibilidad_pct"),
        "diaria": _df(bq, f"SELECT * FROM {base}.{config.TABLAS['diaria']}` ORDER BY dia, dispositivo_id"),
        "calidad": _df(
            bq,
            f"SELECT chequeo, severidad, valor, umbral, resultado FROM {base}.{config.TABLAS['calidad']}` ORDER BY severidad, chequeo",
        ),
    }


if __name__ == "__main__":
    for nombre, df in cargar().items():
        print(f"{nombre}: {len(df)} filas, columnas {list(df.columns)}")
