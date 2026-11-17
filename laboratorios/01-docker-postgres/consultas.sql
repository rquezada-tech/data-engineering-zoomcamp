-- Consultas del laboratorio 1. Ejecútalas con:
--   docker compose exec -T postgres psql -U estudiante -d clima < consultas.sql

-- 1. ¿Cuántas lecturas hay por estación?
SELECT estacion_id, zona, COUNT(*) AS lecturas
FROM lecturas
GROUP BY estacion_id, zona
ORDER BY estacion_id;

-- 2. Temperatura promedio, mínima y máxima por zona
SELECT zona,
       ROUND(AVG(temperatura_c)::numeric, 1) AS promedio,
       MIN(temperatura_c) AS minima,
       MAX(temperatura_c) AS maxima
FROM lecturas
GROUP BY zona
ORDER BY promedio DESC;

-- 3. ¿Qué día llovió más en total (sumando todas las estaciones)?
SELECT DATE(medido_en) AS dia, ROUND(SUM(lluvia_mm)::numeric, 1) AS lluvia_total_mm
FROM lecturas
GROUP BY dia
ORDER BY lluvia_total_mm DESC
LIMIT 1;
