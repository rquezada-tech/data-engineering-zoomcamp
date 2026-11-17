"""Paso 4: hacer preguntas (consultas SQL) a la tabla externa."""
from comun import TABLA_EXTERNA, clientes, ejecutar, tabla, titulo


def mostrar(bq, titulo_consulta, sql):
    print(f"\n» {titulo_consulta}")
    print(sql.strip())
    for fila in bq.query(sql).result():
        print("   ", dict(fila.items()))


def main():
    bq, _ = clientes()
    t = tabla(bq, TABLA_EXTERNA)
    titulo("Paso 4 · Consultar la tabla externa")
    mostrar(bq, "¿Cuántos viajes hay en total?", f"SELECT COUNT(*) AS viajes FROM `{t}`")
    mostrar(
        bq,
        "¿Cuántos viajes hubo por mes?",
        f"""
SELECT FORMAT_TIMESTAMP('%Y-%m', inicio) AS mes, COUNT(*) AS viajes
FROM `{t}`
GROUP BY mes
ORDER BY mes""",
    )
    mostrar(
        bq,
        "¿Qué 3 zonas originan más viajes?",
        f"""
SELECT zona_origen, COUNT(*) AS viajes
FROM `{t}`
GROUP BY zona_origen
ORDER BY viajes DESC
LIMIT 3""",
    )
    mostrar(bq, "¿Cuántos viajes tienen tarifa 0?", f"SELECT COUNT(*) AS viajes_tarifa_cero FROM `{t}` WHERE tarifa = 0")
    print("\nContinúa con: uv run python lab/05_materializar_tabla_interna.py")


if __name__ == "__main__":
    ejecutar(main)
