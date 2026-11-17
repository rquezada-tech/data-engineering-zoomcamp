"""Genera telemetría SINTÉTICA de 12 dispositivos durante 7 días.

Cada dispositivo envía un "latido" (heartbeat) cada 5 minutos con su estado,
temperatura, batería y señal. Para que el proyecto sea realista, el generador
introduce A PROPÓSITO problemas que el pipeline debe detectar:

  * Caídas: DSP-004 se apaga 6 horas; DSP-012 deja de reportar el último día y medio.
  * Conexión inestable: DSP-009 pierde ~8 % de sus latidos al azar.
  * Errores: DSP-007 reporta estado "error" durante 3 horas.
  * Calidad: eventos duplicados, eventos sin dispositivo, temperaturas imposibles
    y relojes desfasados (eventos con fecha en el futuro).

Con la semilla fija, cada ejecución produce exactamente los mismos datos.
Los archivos quedan particionados por fecha, como en un data lake real:
  datos/raw/fecha=2026-11-01/eventos.parquet
"""
from __future__ import annotations

import csv
import random
import shutil
from datetime import datetime, timedelta, timezone

import pyarrow as pa
import pyarrow.parquet as pq

from . import config

ESQUEMA = pa.schema(
    [
        ("evento_id", pa.string()),
        ("dispositivo_id", pa.string()),
        ("ts", pa.timestamp("us", tz="UTC")),
        ("estado", pa.string()),
        ("temperatura_c", pa.float64()),
        ("bateria_pct", pa.float64()),
        ("senal_dbm", pa.int64()),
        ("firmware", pa.string()),
    ]
)

UTC = timezone.utc


def _inicio() -> datetime:
    return datetime.combine(config.FECHA_INICIO, datetime.min.time(), tzinfo=UTC)


def _esta_caido(dispositivo: str, momento: datetime, rng: random.Random) -> bool:
    inicio = _inicio()
    if dispositivo == "DSP-004" and inicio + timedelta(days=2, hours=8) <= momento < inicio + timedelta(days=2, hours=14):
        return True
    if dispositivo == "DSP-012" and momento >= inicio + timedelta(days=5, hours=12):
        return True
    if dispositivo == "DSP-009" and rng.random() < 0.08:
        return True
    return False


def _estado(dispositivo: str, momento: datetime, rng: random.Random) -> str:
    inicio = _inicio()
    if dispositivo == "DSP-007" and inicio + timedelta(days=4, hours=1) <= momento < inicio + timedelta(days=4, hours=4):
        return "error"
    return "degradado" if rng.random() < 0.02 else "ok"


def leer_catalogo() -> list[dict]:
    with open(config.CATALOGO_CSV, newline="") as f:
        return list(csv.DictReader(f))


def generar() -> dict:
    rng = random.Random(2026)
    catalogo = leer_catalogo()
    if config.CARPETA_RAW.exists():
        shutil.rmtree(config.CARPETA_RAW)

    resumen = {"archivos": 0, "filas": 0, "duplicados": 0, "sin_dispositivo": 0, "temp_imposible": 0, "futuro": 0}
    contador = 0
    for d in range(config.DIAS):
        dia = config.FECHA_INICIO + timedelta(days=d)
        filas: list[dict] = []
        for disp in catalogo:
            did = disp["dispositivo_id"]
            temp_base = 22.0 if disp["tipo"] != "sensor_temperatura" else 6.0  # sensores de cámaras de frío
            bateria = 100.0 - d * 1.5
            for i in range(config.LATIDOS_POR_DIA):
                # pequeño "jitter": los latidos no llegan exactamente en el segundo 0
                momento = datetime.combine(dia, datetime.min.time(), tzinfo=UTC) + timedelta(
                    minutes=i * config.INTERVALO_MIN, seconds=rng.randint(0, 20)
                )
                if _esta_caido(did, momento, rng):
                    continue
                contador += 1
                filas.append(
                    {
                        "evento_id": f"EV-{contador:08d}",
                        "dispositivo_id": did,
                        "ts": momento,
                        "estado": _estado(did, momento, rng),
                        "temperatura_c": round(temp_base + rng.gauss(0, 1.2), 2),
                        "bateria_pct": round(max(0.0, bateria - i * 0.002), 2),
                        "senal_dbm": rng.randint(-95, -55),
                        "firmware": "2.4.1" if did != "DSP-010" else "2.3.9",
                    }
                )

        # --- problemas de calidad sembrados a propósito ---
        for fila in rng.sample(filas, 15):  # duplicados exactos (reenvíos del dispositivo)
            filas.append(dict(fila))
            resumen["duplicados"] += 1
        for fila in rng.sample(filas, 3):  # eventos sin dispositivo
            fila["dispositivo_id"] = None
            resumen["sin_dispositivo"] += 1
        for fila in rng.sample(filas, 4):  # sensor dañado: temperatura imposible
            fila["temperatura_c"] = 999.0
            resumen["temp_imposible"] += 1
        for fila in rng.sample(filas, 2):  # reloj desfasado: fecha en el futuro
            fila["ts"] = fila["ts"] + timedelta(days=400)
            resumen["futuro"] += 1

        filas.sort(key=lambda f: (f["ts"], f["evento_id"]))
        destino = config.CARPETA_RAW / f"fecha={dia.isoformat()}" / "eventos.parquet"
        destino.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(pa.Table.from_pylist(filas, schema=ESQUEMA), destino)
        resumen["archivos"] += 1
        resumen["filas"] += len(filas)
    return resumen


def main():
    r = generar()
    print(f"Generados {r['archivos']} archivos con {r['filas']} eventos en {config.CARPETA_RAW}")
    print(
        f"Problemas sembrados: {r['duplicados']} duplicados, {r['sin_dispositivo']} sin dispositivo, "
        f"{r['temp_imposible']} temperaturas imposibles, {r['futuro']} con fecha futura"
    )


if __name__ == "__main__":
    main()
