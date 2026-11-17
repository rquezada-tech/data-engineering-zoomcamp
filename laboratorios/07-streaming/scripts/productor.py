"""Envía lecturas SINTÉTICAS de sensores de temperatura al tópico de Redpanda.

Cada mensaje es un JSON como:
  {"sensor_id": "sensor-01", "temperatura": 21.37, "ts": 1704110400000}

`ts` es la hora del EVENTO (cuándo midió el sensor), en milisegundos desde 1970.
Las horas son fijas (1 de enero de 2024, 12:00 UTC en adelante) para que todos
obtengan los mismos resultados, sin importar a qué hora ejecutes el script.
"""
import argparse
import json
import random
import time

from kafka import KafkaProducer

INICIO_MS = 1_704_110_400_000  # 2024-01-01 12:00:00 UTC
SENSORES = [f"sensor-{n:02d}" for n in range(1, 6)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--servidor", default="127.0.0.1:9092")
    p.add_argument("--topico", default="lecturas-sensores")
    p.add_argument("--minutos", type=int, default=10, help="minutos de 'tiempo de evento' a simular")
    p.add_argument("--pausa", type=float, default=0.0, help="segundos de espera entre mensajes (0 = lo más rápido posible)")
    p.add_argument("--sin-cierre", action="store_true", help="no enviar el evento final que cierra la última ventana")
    args = p.parse_args()

    productor = KafkaProducer(bootstrap_servers=args.servidor)

    def enviar(clave, valor):
        # Kafka guarda bytes: convertimos el diccionario a texto JSON y luego a bytes.
        productor.send(args.topico, key=clave.encode("utf-8"), value=json.dumps(valor).encode("utf-8"))

    rng = random.Random(7)
    enviados = 0
    t0 = time.time()
    # Una lectura cada 5 segundos por sensor -> 12 lecturas por sensor por minuto.
    for paso in range(args.minutos * 12):
        for sensor in SENSORES:
            evento = {
                "sensor_id": sensor,
                "temperatura": round(20 + rng.gauss(0, 2), 2),
                "ts": INICIO_MS + paso * 5_000,
            }
            enviar(sensor, evento)
            enviados += 1
            if args.pausa:
                time.sleep(args.pausa)
    # Un último evento 2 minutos "en el futuro" para que Flink sepa que puede cerrar las ventanas pendientes.
    if not args.sin_cierre:
        enviar("cierre", {"sensor_id": "cierre", "temperatura": 0.0, "ts": INICIO_MS + (args.minutos + 2) * 60_000})
    productor.flush()
    print(f"Enviados {enviados} eventos" + ("" if args.sin_cierre else " + 1 de cierre") + f" al tópico '{args.topico}' en {time.time() - t0:.2f} s")


if __name__ == "__main__":
    main()
