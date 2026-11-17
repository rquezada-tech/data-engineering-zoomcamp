"""Pruebas del generador: no necesitan LocalCloud."""
import pyarrow.compute as pc
import pyarrow.parquet as pq

from telemetria import config, generar


def test_generador_es_determinista_y_siembra_problemas():
    r1 = generar.generar()
    r2 = generar.generar()
    assert r1 == r2, "con la misma semilla deben salir los mismos datos"
    assert r1["archivos"] == config.DIAS
    assert r1["duplicados"] == 15 * config.DIAS
    assert r1["sin_dispositivo"] == 3 * config.DIAS
    assert r1["temp_imposible"] == 4 * config.DIAS
    assert r1["futuro"] == 2 * config.DIAS


def test_caidas_sembradas():
    generar.generar()
    t = pq.read_table(config.CARPETA_RAW)
    por_disp = {d: 0 for d in ["DSP-001", "DSP-004", "DSP-012"]}
    for d in por_disp:
        por_disp[d] = t.filter(pc.equal(t["dispositivo_id"], d)).num_rows
    # DSP-001 está sano: ~288 por día; DSP-004 pierde 6 h; DSP-012 pierde 1,5 días.
    assert por_disp["DSP-001"] > por_disp["DSP-004"] > por_disp["DSP-012"]
