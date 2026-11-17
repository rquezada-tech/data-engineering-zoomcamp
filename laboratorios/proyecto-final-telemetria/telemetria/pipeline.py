"""Ejecuta el pipeline completo, paso por paso, mostrando qué pasa en cada uno.

Uso:
    uv run python -m telemetria.pipeline            # todos los pasos
    uv run python -m telemetria.pipeline calidad     # solo un paso (y los anteriores deben existir)

Pasos, en orden:  generar -> ingestar -> warehouse -> calidad -> metricas
"""
from __future__ import annotations

import sys
import time

from . import generar, pasos
from .conexion import clientes, detener, ejecutar, titulo

ORDEN = ["generar", "ingestar", "warehouse", "calidad", "metricas"]


def _mostrar_calidad(r: dict) -> None:
    for c in r["chequeos"]:
        icono = {"OK": "✅", "ALERTA": "⚠️ ", "FALLA": "❌"}[c["resultado"]]
        print(f"   {icono} {c['chequeo']:36s} valor={c['valor']:<8g} umbral {c['umbral']:<12s} [{c['severidad']}]")


def _mostrar_metricas(r: dict) -> None:
    print(f"   {'dispositivo':12s} {'sitio':15s} {'disponib.':>9s} {'min sin señal':>14s}  objetivo")
    for d in r["dispositivos"]:
        print(
            f"   {d['dispositivo_id']:12s} {d['sitio']:15s} {d['disponibilidad_pct']:>8.2f}% "
            f"{d['minutos_sin_senal']:>14d}  {'cumple' if d['cumple_objetivo'] else 'NO cumple'}"
        )


def correr(seleccion: list[str]) -> None:
    bq = gcs = None
    for paso in seleccion:
        inicio = time.time()
        titulo(f"Paso: {paso}")
        if paso == "generar":
            r = generar.generar()
            print(f"   {r['filas']} eventos en {r['archivos']} archivos Parquet (datos/raw/fecha=.../)")
            print(f"   problemas sembrados: {r['duplicados']} duplicados, {r['sin_dispositivo']} sin dispositivo, "
                  f"{r['temp_imposible']} temperaturas imposibles, {r['futuro']} con fecha futura")
        else:
            if bq is None:
                bq, gcs = clientes()
            r = getattr(pasos, {"ingestar": "ingestar", "warehouse": "cargar_warehouse",
                                "calidad": "controlar_calidad", "metricas": "calcular_metricas"}[paso])(bq, gcs)
            if paso == "calidad":
                _mostrar_calidad(r)
                if r["fallas_criticas"]:
                    detener(f"{r['fallas_criticas']} control(es) de calidad CRÍTICO(s) fallaron. "
                            "No se calculan métricas sobre datos malos. Revisa la tabla calidad_resultados.")
            elif paso == "metricas":
                _mostrar_metricas(r)
            else:
                for k, v in r.items():
                    print(f"   {k}: {v}")
        print(f"   ({time.time() - inicio:.1f} s)")
    print("\nPIPELINE OK ✅  Abre el dashboard con: uv run streamlit run dashboard/app.py")


def main():
    args = sys.argv[1:]
    desconocidos = [a for a in args if a not in ORDEN]
    if desconocidos:
        detener(f"Paso desconocido: {desconocidos}. Pasos válidos: {', '.join(ORDEN)}")
    ejecutar(lambda: correr(args or ORDEN))


if __name__ == "__main__":
    main()
