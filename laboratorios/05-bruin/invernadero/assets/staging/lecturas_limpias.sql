/* @bruin

name: staging.lecturas_limpias
type: duckdb.sql
description: Lecturas válidas, con el nombre del cultivo. Se descartan las lecturas sin temperatura.

depends:
  - ingesta.lecturas
  - ingesta.invernaderos

materialization:
  type: table

columns:
  - name: lectura_id
    type: varchar
    primary_key: true
    checks:
      - name: not_null
      - name: unique
  - name: invernadero_id
    type: varchar
    checks:
      - name: not_null
      - name: accepted_values
        value: [INV-1, INV-2, INV-3]
  - name: temperatura_c
    type: double
    checks:
      - name: not_null
  - name: humedad_pct
    type: double
    checks:
      - name: non_negative
      - name: max
        value: 100

custom_checks:
  - name: no hay lecturas en el futuro
    query: SELECT COUNT(*) FROM staging.lecturas_limpias WHERE medido_en > now()
    value: 0

@bruin */

SELECT
    l.lectura_id,
    l.invernadero_id,
    i.cultivo,
    l.sensor_id,
    l.medido_en,
    CAST(l.medido_en AS DATE) AS fecha,
    l.temperatura_c,
    l.humedad_pct
FROM ingesta.lecturas AS l
JOIN ingesta.invernaderos AS i USING (invernadero_id)
WHERE l.temperatura_c IS NOT NULL
