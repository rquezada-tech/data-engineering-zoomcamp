"""Paso 1: generar archivos Parquet pequeños con viajes SINTÉTICOS (inventados).

No se descarga nada de internet. Usamos una "semilla" fija (42) para que todas
las personas obtengan exactamente los mismos datos y los mismos resultados.
"""
import random
from datetime import datetime, timedelta, timezone

import pyarrow as pa
import pyarrow.parquet as pq

from comun import CARPETA_DATOS, MESES, ejecutar, titulo

ZONAS = ["Centro", "Norte", "Sur", "Oriente", "Poniente", "Aeropuerto", "Puerto", "Universidad"]
PESOS_ZONAS = [30, 12, 12, 15, 10, 8, 5, 8]  # el Centro es la zona con más viajes
TIPOS_PAGO = ["tarjeta", "efectivo", "app"]
VIAJES_POR_MES = 2000

ESQUEMA = pa.schema(
    [
        ("viaje_id", pa.int64()),
        ("inicio", pa.timestamp("us", tz="UTC")),
        ("fin", pa.timestamp("us", tz="UTC")),
        ("zona_origen", pa.string()),
        ("distancia_km", pa.float64()),
        ("tarifa", pa.float64()),
        ("propina", pa.float64()),
        ("tipo_pago", pa.string()),
    ]
)


def generar_mes(rng: random.Random, mes: str, primer_id: int) -> pa.Table:
    anio, num_mes = (int(x) for x in mes.split("-"))
    # Fechas en UTC: así BigQuery las reconoce como TIMESTAMP (fecha + hora + zona horaria).
    comienzo = datetime(anio, num_mes, 1, tzinfo=timezone.utc)
    fin_mes = datetime(anio + (num_mes == 12), num_mes % 12 + 1, 1, tzinfo=timezone.utc)
    segundos_mes = int((fin_mes - comienzo).total_seconds())
    filas = {campo: [] for campo in ESQUEMA.names}
    for i in range(VIAJES_POR_MES):
        inicio = comienzo + timedelta(seconds=rng.randrange(segundos_mes))
        distancia = round(rng.uniform(0.5, 25.0), 2)
        minutos = distancia * rng.uniform(2.0, 4.0)
        tarifa = round(1.5 + distancia * 0.9, 2)
        if rng.random() < 0.01:  # ~1% de viajes con tarifa 0 (cortesías o errores de registro)
            tarifa = 0.0
        pago = rng.choice(TIPOS_PAGO)
        propina = round(tarifa * rng.uniform(0.0, 0.2), 2) if pago != "efectivo" else 0.0
        filas["viaje_id"].append(primer_id + i)
        filas["inicio"].append(inicio)
        filas["fin"].append(inicio + timedelta(minutes=minutos))
        filas["zona_origen"].append(rng.choices(ZONAS, weights=PESOS_ZONAS)[0])
        filas["distancia_km"].append(distancia)
        filas["tarifa"].append(tarifa)
        filas["propina"].append(propina)
        filas["tipo_pago"].append(pago)
    return pa.table(filas, schema=ESQUEMA)


def main():
    titulo("Paso 1 · Generar Parquet sintético")
    CARPETA_DATOS.mkdir(exist_ok=True)
    rng = random.Random(42)
    total = 0
    for n, mes in enumerate(MESES):
        tabla = generar_mes(rng, mes, primer_id=n * VIAJES_POR_MES + 1)
        destino = CARPETA_DATOS / f"viajes_{mes}.parquet"
        pq.write_table(tabla, destino)
        total += tabla.num_rows
        print(f"  {destino.name}: {tabla.num_rows} filas, {destino.stat().st_size / 1024:.0f} KB")
    print(f"\nTotal: {total} viajes en {len(MESES)} archivos dentro de {CARPETA_DATOS.name}/")
    print("Continúa con: uv run python lab/02_subir_a_bucket.py")


if __name__ == "__main__":
    ejecutar(main)
