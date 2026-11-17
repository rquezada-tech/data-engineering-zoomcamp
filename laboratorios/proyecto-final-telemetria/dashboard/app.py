"""Dashboard de disponibilidad de dispositivos.

Ejecutar desde la carpeta del proyecto:
    uv run streamlit run dashboard/app.py

Lee las tablas que deja el pipeline en BigQuery LOCAL (LocalCloud).
"""
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from telemetria import config  # noqa: E402
from telemetria.datos_dashboard import cargar  # noqa: E402

st.set_page_config(page_title="Disponibilidad de dispositivos", page_icon="📡", layout="wide")


@st.cache_data(ttl=60)
def datos() -> dict[str, pd.DataFrame]:
    return cargar()


try:
    d = datos()
except SystemExit:
    st.error(
        "No pude leer los datos desde LocalCloud. Revisa que el emulador esté encendido "
        "y que hayas ejecutado el pipeline: `uv run python -m telemetria.pipeline`."
    )
    st.stop()

resumen, diaria, calidad = d["resumen"], d["diaria"], d["calidad"]
resumen["cumple"] = resumen["cumple_objetivo"].map({True: "Sí", False: "No"})

st.title("📡 Disponibilidad de dispositivos")
st.caption(
    f"Datos sintéticos · {len(diaria['dia'].unique())} días desde el {config.FECHA_INICIO:%d-%m-%Y} · "
    f"objetivo de disponibilidad: {config.OBJETIVO_DISPONIBILIDAD:.0f} % · fuente: BigQuery local (LocalCloud)"
)

# --- Indicadores principales -------------------------------------------------
global_pct = 100 * diaria["intervalos_operativos"].sum() / diaria["intervalos_esperados"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Disponibilidad global", f"{global_pct:.2f} %")
c2.metric("Dispositivos", len(resumen))
c3.metric("Bajo el objetivo", int((~resumen["cumple_objetivo"]).sum()))
c4.metric("Horas sin señal (total)", f"{resumen['minutos_sin_senal'].sum() / 60:.1f}")

# --- Disponibilidad por dispositivo (distribución por categoría) -------------
st.subheader("Disponibilidad por dispositivo")
barras = (
    alt.Chart(resumen)
    .mark_bar(clip=True)  # clip: no dibujar fuera del eje (empieza en 70 %)
    .encode(
        x=alt.X("disponibilidad_pct:Q", title="Disponibilidad (%)", scale=alt.Scale(domain=[70, 100])),
        y=alt.Y("dispositivo_id:N", sort="x", title=None),
        color=alt.Color(
            "cumple:N",
            title="¿Cumple objetivo?",
            scale=alt.Scale(domain=["Sí", "No"], range=["#2f7d4f", "#c0392b"]),
        ),
        tooltip=["dispositivo_id", "sitio", "tipo", "disponibilidad_pct", "minutos_sin_senal"],
    )
)
regla = alt.Chart(pd.DataFrame({"x": [config.OBJETIVO_DISPONIBILIDAD]})).mark_rule(strokeDash=[4, 4]).encode(x="x:Q")
st.altair_chart(barras + regla, width="stretch")

# --- Evolución diaria por sitio (serie de tiempo) -----------------------------
st.subheader("Disponibilidad diaria por sitio")
por_sitio = (
    diaria.groupby(["dia", "sitio"], as_index=False)[["intervalos_operativos", "intervalos_esperados"]]
    .sum()
    .assign(disponibilidad_pct=lambda x: 100 * x["intervalos_operativos"] / x["intervalos_esperados"])
)
linea = (
    alt.Chart(por_sitio)
    .mark_line(point=True)
    .encode(
        x=alt.X("dia:T", title="Día"),
        y=alt.Y("disponibilidad_pct:Q", title="Disponibilidad (%)", scale=alt.Scale(zero=False)),
        color=alt.Color("sitio:N", title="Sitio"),
        tooltip=["dia:T", "sitio", alt.Tooltip("disponibilidad_pct:Q", format=".2f")],
    )
)
st.altair_chart(linea, width="stretch")

# --- Detalle y calidad --------------------------------------------------------
izq, der = st.columns(2)
with izq:
    st.subheader("Detalle por dispositivo")
    st.dataframe(resumen, hide_index=True, width="stretch")
with der:
    st.subheader("Controles de calidad de la última ejecución")
    st.dataframe(calidad, hide_index=True, width="stretch")
