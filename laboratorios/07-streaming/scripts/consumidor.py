"""Lee mensajes del tópico y muestra algunos en pantalla (para ver qué hay adentro)."""
import argparse
import json

from kafka import KafkaConsumer


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--servidor", default="127.0.0.1:9092")
    p.add_argument("--topico", default="lecturas-sensores")
    p.add_argument("--cantidad", type=int, default=5)
    args = p.parse_args()

    consumidor = KafkaConsumer(
        args.topico,
        bootstrap_servers=args.servidor,
        auto_offset_reset="earliest",   # empezar desde el primer mensaje guardado
        enable_auto_commit=False,       # no marcamos nada como "leído": puedes repetirlo
        consumer_timeout_ms=10_000,     # si en 10 s no llega nada, terminamos
    )
    total = 0
    temp_alta = 0
    for msg in consumidor:
        valor = json.loads(msg.value.decode("utf-8"))  # bytes -> texto JSON -> diccionario
        total += 1
        if valor["temperatura"] > 23:
            temp_alta += 1
        if total <= args.cantidad:
            print(f"particion={msg.partition} offset={msg.offset} valor={valor}")
    print(f"\nMensajes leídos: {total}. Lecturas con temperatura > 23 °C: {temp_alta}")


if __name__ == "__main__":
    main()
