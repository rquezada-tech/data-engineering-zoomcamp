"""Taller de ingesta con dlt (data load tool).

Simulamos una "API" de una tienda que entrega pedidos en páginas de 50.
dlt se encarga de:
  * pedir página tras página hasta que no queden datos,
  * crear las tablas en DuckDB (adivinando los tipos de cada columna),
  * recordar hasta qué fecha cargó (carga incremental), para que la próxima
    vez solo traiga pedidos nuevos.

Uso:
    uv run python pipeline.py --dias 3     # primera carga: días 1 a 3
    uv run python pipeline.py --dias 5     # segunda carga: solo trae días 4 y 5
"""

import argparse
import random
from datetime import datetime, timedelta, timezone

import dlt

INICIO = datetime(2024, 1, 1, tzinfo=timezone.utc)
PEDIDOS_POR_DIA = 120
TAMANO_PAGINA = 50
PRODUCTOS = ["teclado", "mouse", "monitor", "audífonos", "cable usb", "notebook"]
CIUDADES = ["Santiago", "Lima", "Bogotá", "Ciudad de México", "Buenos Aires", "Quito"]


# ---------------------------------------------------------------------------
# 1) La "API" falsa. En la vida real esto sería una URL; aquí es una función.
# ---------------------------------------------------------------------------
def api_falsa_pedidos(desde: datetime, dias_disponibles: int, pagina: int) -> list[dict]:
    """Devuelve una página de pedidos creados DESPUÉS de `desde`.

    `dias_disponibles` simula el paso del tiempo: cuántos días de pedidos existen hoy.
    Si la página viene vacía, significa que no hay más datos.
    """
    todos = []
    for n in range(dias_disponibles * PEDIDOS_POR_DIA):
        rng = random.Random(n)  # misma semilla => mismo pedido en cada ejecución
        creado = INICIO + timedelta(minutes=n * (24 * 60 / PEDIDOS_POR_DIA))
        if creado <= desde:
            continue
        cantidad = rng.randint(1, 4)
        precio = rng.choice([9.9, 19.9, 49.9, 199.0, 899.0])
        todos.append(
            {
                "pedido_id": n + 1,
                "creado_en": creado.isoformat(),
                "cliente_id": rng.randint(1, 40),
                "producto": rng.choice(PRODUCTOS),
                "cantidad": cantidad,
                "precio_unitario": precio,
                "envio": {"ciudad": rng.choice(CIUDADES), "express": rng.random() < 0.3},
            }
        )
    inicio = pagina * TAMANO_PAGINA
    return todos[inicio : inicio + TAMANO_PAGINA]


# ---------------------------------------------------------------------------
# 2) Los "recursos" de dlt: cada uno termina siendo una tabla.
# ---------------------------------------------------------------------------
@dlt.resource(name="pedidos", primary_key="pedido_id", write_disposition="merge")
def pedidos(
    dias_disponibles: int,
    creado_en=dlt.sources.incremental("creado_en", initial_value="2023-12-31T23:59:59+00:00"),
):
    """Lee la API página por página. `creado_en.last_value` es la fecha del último pedido ya cargado."""
    desde = datetime.fromisoformat(creado_en.last_value)
    pagina = 0
    while True:
        lote = api_falsa_pedidos(desde, dias_disponibles, pagina)
        if not lote:  # página vacía => terminamos
            break
        print(f"  página {pagina}: {len(lote)} pedidos")
        yield lote
        pagina += 1


@dlt.resource(name="clientes", primary_key="cliente_id", write_disposition="replace")
def clientes():
    """Tabla pequeña que se reemplaza completa en cada carga."""
    for cliente_id in range(1, 41):
        rng = random.Random(10_000 + cliente_id)
        yield {"cliente_id": cliente_id, "segmento": rng.choice(["nuevo", "frecuente", "empresa"])}


@dlt.source(name="tienda")
def fuente_tienda(dias_disponibles: int):
    return pedidos(dias_disponibles), clientes()


def main():
    parser = argparse.ArgumentParser(description="Carga pedidos sintéticos a DuckDB con dlt")
    parser.add_argument("--dias", type=int, default=3, help="cuántos días de pedidos 'existen' hoy en la API")
    args = parser.parse_args()

    pipeline = dlt.pipeline(
        pipeline_name="tienda_local",
        destination=dlt.destinations.duckdb("tienda_local.duckdb"),  # archivo en esta carpeta
        dataset_name="tienda",
        pipelines_dir=".dlt_pipelines",  # estado del pipeline dentro de esta carpeta
    )
    print(f"Cargando pedidos de la API falsa (días disponibles: {args.dias})...")
    info = pipeline.run(fuente_tienda(args.dias))
    print(info)
    filas = pipeline.last_trace.last_normalize_info.row_counts
    print("\nFilas cargadas en ESTA ejecución:")
    for tabla, n in sorted(filas.items()):
        if not tabla.startswith("_dlt"):
            print(f"  {tabla}: {n}")


if __name__ == "__main__":
    main()
