"""@bruin

name: ingesta.lecturas
type: python
image: python:3.12
connection: duckdb-local
description: |
  Lecturas SINTÉTICAS de sensores de temperatura y humedad.
  Genera datos solo para el rango de fechas de la ejecución (--start-date / --end-date).
  Alrededor de un 2 % de las lecturas vienen sin temperatura (sensor con falla).

materialization:
  type: table

columns:
  - name: lectura_id
    type: varchar
    primary_key: true
  - name: invernadero_id
    type: varchar
  - name: sensor_id
    type: varchar
  - name: medido_en
    type: timestamp
  - name: temperatura_c
    type: double
  - name: humedad_pct
    type: double

@bruin"""

import json
import math
import os
import random
from datetime import datetime, timedelta

import pandas as pd

INVERNADEROS = {"INV-1": 24.0, "INV-2": 18.0, "INV-3": 21.0}  # temperatura media de cada uno


def materialize():
    # Bruin entrega el rango de fechas y las variables como variables de entorno.
    inicio = datetime.fromisoformat(os.environ["BRUIN_START_DATE"])
    fin = datetime.fromisoformat(os.environ["BRUIN_END_DATE"]) + timedelta(days=1)
    variables = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    por_hora = int(variables.get("lecturas_por_hora", 4))
    paso = timedelta(minutes=60 // por_hora)

    filas = []
    momento = inicio
    while momento < fin:
        for inv, media in INVERNADEROS.items():
            for sensor in (1, 2):
                rng = random.Random(f"{inv}-{sensor}-{momento.isoformat()}")  # determinista
                hora = momento.hour + momento.minute / 60
                ciclo = 8 * math.sin((hora - 9) / 24 * 2 * math.pi)  # más calor a media tarde
                temperatura = round(media + ciclo + rng.gauss(0, 1.5), 2)
                filas.append(
                    {
                        "lectura_id": f"{inv}-S{sensor}-{momento:%Y%m%d%H%M}",
                        "invernadero_id": inv,
                        "sensor_id": f"{inv}-S{sensor}",
                        "medido_en": momento,
                        "temperatura_c": None if rng.random() < 0.02 else temperatura,
                        "humedad_pct": round(min(100, max(0, 70 - ciclo * 2 + rng.gauss(0, 4))), 1),
                    }
                )
        momento += paso
    print(f"Generadas {len(filas)} lecturas entre {inicio:%Y-%m-%d} y {fin:%Y-%m-%d} (excluido)")
    return pd.DataFrame(filas)
