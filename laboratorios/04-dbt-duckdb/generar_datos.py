"""Genera viajes SINTÉTICOS (inventados) en Parquet dentro de datos/.

Usa una semilla fija, así que todas las personas obtienen exactamente los mismos datos.
Uso:  uv run python generar_datos.py
"""
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

CARPETA = Path(__file__).parent / "datos"
MESES = ["2024-01", "2024-02", "2024-03"]
VIAJES_POR_MES = 2000
ZONAS = ["Centro", "Norte", "Sur", "Oriente", "Poniente", "Aeropuerto", "Puerto", "Universidad"]
PESOS = [30, 12, 12, 15, 10, 8, 5, 8]
PAGOS = [1, 2, 3]  # 1 = tarjeta, 2 = efectivo, 3 = app (ver seeds/tipos_pago.csv)

ESQUEMA = pa.schema(
    [
        ("viaje_id", pa.int64()),
        ("inicio", pa.timestamp("us", tz="UTC")),
        ("fin", pa.timestamp("us", tz="UTC")),
        ("zona_origen", pa.string()),
        ("zona_destino", pa.string()),
        ("distancia_km", pa.float64()),
        ("tarifa", pa.float64()),
        ("propina", pa.float64()),
        ("tipo_pago", pa.int64()),
    ]
)


def main():
    CARPETA.mkdir(exist_ok=True)
    rng = random.Random(2024)
    viaje_id = 1
    for mes in MESES:
        anio, m = (int(x) for x in mes.split("-"))
        comienzo = datetime(anio, m, 1, tzinfo=timezone.utc)
        siguiente = datetime(anio + (m == 12), m % 12 + 1, 1, tzinfo=timezone.utc)
        segundos = int((siguiente - comienzo).total_seconds())
        filas = {c: [] for c in ESQUEMA.names}
        for _ in range(VIAJES_POR_MES):
            inicio = comienzo + timedelta(seconds=rng.randrange(segundos))
            distancia = round(rng.uniform(0.5, 25.0), 2)
            tarifa = round(1.5 + distancia * 0.9, 2)
            if rng.random() < 0.01:  # ~1 % de registros con tarifa 0: los limpiaremos en dbt
                tarifa = 0.0
            pago = rng.choice(PAGOS)
            filas["viaje_id"].append(viaje_id)
            filas["inicio"].append(inicio)
            filas["fin"].append(inicio + timedelta(minutes=distancia * rng.uniform(2.0, 4.0)))
            filas["zona_origen"].append(rng.choices(ZONAS, weights=PESOS)[0])
            filas["zona_destino"].append(rng.choices(ZONAS, weights=PESOS)[0])
            filas["distancia_km"].append(distancia)
            filas["tarifa"].append(tarifa)
            filas["propina"].append(round(tarifa * rng.uniform(0, 0.2), 2) if pago != 2 else 0.0)
            filas["tipo_pago"].append(pago)
            viaje_id += 1
        destino = CARPETA / f"viajes_{mes}.parquet"
        pq.write_table(pa.table(filas, schema=ESQUEMA), destino)
        print(f"{destino.relative_to(Path(__file__).parent)}: {VIAJES_POR_MES} viajes")


if __name__ == "__main__":
    main()
