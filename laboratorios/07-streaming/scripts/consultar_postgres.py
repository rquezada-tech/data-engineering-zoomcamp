"""Muestra lo que Flink escribió en PostgreSQL."""
import psycopg

CONEXION = "host=localhost port=5433 dbname=streaming user=postgres password=postgres"

with psycopg.connect(CONEXION) as con:
    total = con.execute("SELECT COUNT(*), COUNT(DISTINCT ventana_inicio), COUNT(DISTINCT sensor_id) FROM lecturas_por_minuto").fetchone()
    print(f"Filas: {total[0]} | ventanas de 1 minuto: {total[1]} | sensores: {total[2]}")
    for fila in con.execute(
        "SELECT ventana_inicio, sensor_id, lecturas, ROUND(temp_promedio::numeric, 2), temp_maxima "
        "FROM lecturas_por_minuto ORDER BY ventana_inicio, sensor_id LIMIT 6"
    ):
        print(fila)
