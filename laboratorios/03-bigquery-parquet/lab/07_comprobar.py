"""Paso 7: comprobar automáticamente que todo quedó bien.

Compara lo que dicen los archivos Parquet de tu disco con lo que responde BigQuery local.
Si todo cuadra imprime "LABORATORIO OK" y termina con código 0.
"""
import sys

import pyarrow.compute as pc
import pyarrow.parquet as pq

from comun import (
    CARPETA_DATOS,
    MESES,
    TABLA_EXTERNA,
    TABLA_INTERNA,
    TABLA_PARTICIONADA,
    clientes,
    ejecutar,
    tabla,
    titulo,
)


def main():
    bq, _ = clientes()
    titulo("Paso 7 · Comprobaciones automáticas")
    local = pq.read_table(CARPETA_DATOS)  # lee todos los Parquet de la carpeta datos/
    esperado_total = local.num_rows
    esperado_validos = local.filter(pc.greater(local["tarifa"], 0)).num_rows
    esperado_suma = round(pc.sum(local.filter(pc.greater(local["tarifa"], 0))["tarifa"]).as_py(), 2)

    def uno(sql):
        return list(bq.query(sql).result())[0][0]

    chequeos = [
        ("Archivos Parquet generados", len(list(CARPETA_DATOS.glob("viajes_*.parquet"))), len(MESES)),
        ("Filas en la tabla externa", uno(f"SELECT COUNT(*) FROM `{tabla(bq, TABLA_EXTERNA)}`"), esperado_total),
        ("Filas en la tabla interna", uno(f"SELECT COUNT(*) FROM `{tabla(bq, TABLA_INTERNA)}`"), esperado_validos),
        (
            "Suma de tarifas (tabla interna)",
            round(uno(f"SELECT SUM(tarifa) FROM `{tabla(bq, TABLA_INTERNA)}`"), 2),
            esperado_suma,
        ),
        ("Tipo de la tabla externa", bq.get_table(tabla(bq, TABLA_EXTERNA)).table_type, "EXTERNAL"),
        ("Tipo de la tabla interna", bq.get_table(tabla(bq, TABLA_INTERNA)).table_type, "TABLE"),
        (
            "Filas en la tabla particionada",
            uno(f"SELECT COUNT(*) FROM `{tabla(bq, TABLA_PARTICIONADA)}`"),
            esperado_validos,
        ),
        ("Clustering de la tabla particionada", bq.get_table(tabla(bq, TABLA_PARTICIONADA)).clustering_fields, ["zona_origen"]),
    ]
    fallas = 0
    for nombre, obtenido, esperado in chequeos:
        ok = obtenido == esperado
        fallas += not ok
        print(f"  [{'OK' if ok else 'FALLA'}] {nombre}: {obtenido}" + ("" if ok else f" (se esperaba {esperado})"))

    if fallas:
        print(f"\n{fallas} comprobación(es) fallaron. Repite los pasos desde el 1 o ejecuta ./ejecutar_lab.sh")
        sys.exit(1)
    print("\nLABORATORIO OK ✅")


if __name__ == "__main__":
    ejecutar(main)
