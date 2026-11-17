"""Revisa qué quedó en DuckDB después de correr pipeline.py."""
from pathlib import Path

import duckdb

ARCHIVO = Path(__file__).parent / "tienda_local.duckdb"
if not ARCHIVO.exists():
    raise SystemExit("No existe tienda_local.duckdb. Primero ejecuta: uv run python pipeline.py --dias 3")

con = duckdb.connect(str(ARCHIVO), read_only=True)
con.sql("SET TimeZone = 'UTC'")  # mostramos las fechas en UTC, igual que en la fuente


def mostrar(titulo, sql):
    print(f"\n» {titulo}")
    filas = con.sql(sql).fetchall()
    columnas = [c[0] for c in con.sql(sql).description]
    print("   " + " | ".join(columnas))
    for fila in filas:
        print("   " + " | ".join(str(v) for v in fila))


mostrar("Tablas creadas por dlt", "SELECT table_name FROM information_schema.tables WHERE table_schema = 'tienda' ORDER BY 1")
mostrar(
    "Cuántos pedidos hay y qué rango de fechas cubren",
    "SELECT COUNT(*) AS pedidos, MIN(creado_en) AS primero, MAX(creado_en) AS ultimo FROM tienda.pedidos",
)
mostrar("¿Hay pedidos duplicados? (debería ser 0)", "SELECT COUNT(*) - COUNT(DISTINCT pedido_id) AS duplicados FROM tienda.pedidos")
mostrar(
    "Columnas de pedidos (fíjate cómo 'envio' se aplanó en envio__ciudad y envio__express)",
    "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='tienda' AND table_name='pedidos' ORDER BY ordinal_position",
)
mostrar(
    "Ventas por ciudad",
    """SELECT envio__ciudad AS ciudad, COUNT(*) AS pedidos, ROUND(SUM(cantidad * precio_unitario), 2) AS ventas
       FROM tienda.pedidos GROUP BY 1 ORDER BY ventas DESC""",
)
mostrar(
    "Historial de cargas (_dlt_loads): una fila por cada vez que corriste el pipeline",
    "SELECT load_id, status, inserted_at FROM tienda._dlt_loads ORDER BY inserted_at",
)
