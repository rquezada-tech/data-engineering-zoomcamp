/* @bruin

name: reportes.resumen_diario
type: duckdb.sql
description: |
  Resumen por invernadero y día. Cuenta como "alerta" cada lectura sobre el umbral
  definido en la variable umbral_temperatura_c.

depends:
  - staging.lecturas_limpias

materialization:
  type: table

columns:
  - name: fecha
    type: date
    checks:
      - name: not_null
  - name: lecturas
    type: integer
    checks:
      - name: positive

@bruin */

SELECT
    fecha,
    invernadero_id,
    cultivo,
    COUNT(*) AS lecturas,
    ROUND(AVG(temperatura_c), 2) AS temperatura_promedio_c,
    MAX(temperatura_c) AS temperatura_maxima_c,
    COUNT(*) FILTER (WHERE temperatura_c > {{ var.umbral_temperatura_c }}) AS alertas_calor,
    {{ var.umbral_temperatura_c }} AS umbral_usado_c
FROM staging.lecturas_limpias
GROUP BY fecha, invernadero_id, cultivo
ORDER BY fecha, invernadero_id
