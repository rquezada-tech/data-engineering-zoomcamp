"""Prueba de integración: corre el pipeline completo contra LocalCloud.

Si LocalCloud no está encendido, la prueba se SALTA (no falla) y lo dice.
"""
import urllib.request

import pytest

from telemetria import pipeline, pasos
from telemetria.conexion import clientes


def _localcloud_activo() -> bool:
    try:
        with urllib.request.urlopen("http://localhost:5380/readiness", timeout=3):
            return True
    except OSError:
        return False


@pytest.mark.skipif(not _localcloud_activo(), reason="LocalCloud no está encendido")
def test_pipeline_completo():
    pipeline.correr(pipeline.ORDEN)
    bq, gcs = clientes()
    calidad = pasos.controlar_calidad(bq, gcs)
    assert calidad["fallas_criticas"] == 0
    resumen = {d["dispositivo_id"]: d for d in pasos.calcular_metricas(bq, gcs)["dispositivos"]}
    assert len(resumen) == 12
    # Los dispositivos con fallas sembradas no cumplen el objetivo; los sanos sí.
    assert {k for k, d in resumen.items() if not d["cumple_objetivo"]} == {"DSP-004", "DSP-007", "DSP-009", "DSP-012"}
    assert resumen["DSP-012"]["disponibilidad_pct"] == pytest.approx(78.27, abs=0.01)
