"""Muestra qué construyó dbt dentro de viajes_locales.duckdb."""
from pathlib import Path

import duckdb

ARCHIVO = Path(__file__).parent / "viajes_locales.duckdb"
if not ARCHIVO.exists():
    raise SystemExit("No existe viajes_locales.duckdb. Primero ejecuta: uv run dbt build --profiles-dir .")

con = duckdb.connect(str(ARCHIVO), read_only=True)
con.sql("SET TimeZone = 'UTC'")

print("» Objetos creados por dbt (schema.tabla y tipo)")
print(con.sql("SELECT table_schema, table_name, table_type FROM information_schema.tables ORDER BY 1, 2"))
print("» Filas en cada capa")
print(
    con.sql(
        """SELECT (SELECT COUNT(*) FROM staging.stg_viajes)            AS staging,
                  (SELECT COUNT(*) FROM intermediate.int_viajes_validos) AS intermedia,
                  (SELECT COUNT(*) FROM marts.fct_viajes)                AS hechos,
                  (SELECT COUNT(*) FROM marts.ingresos_mensuales_por_zona) AS reporte"""
    )
)
print("» Top 3 zonas por ingresos en enero 2024")
print(
    con.sql(
        """SELECT mes, zona, viajes, ingresos_totales
           FROM marts.ingresos_mensuales_por_zona
           WHERE mes = DATE '2024-01-01'
           ORDER BY ingresos_totales DESC LIMIT 3"""
    )
)
