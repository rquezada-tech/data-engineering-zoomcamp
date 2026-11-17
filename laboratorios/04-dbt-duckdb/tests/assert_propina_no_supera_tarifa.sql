-- Prueba "singular": una consulta que debe devolver CERO filas.
-- Si devuelve alguna, dbt marca la prueba como fallida.
-- Regla: en estos datos la propina nunca debería ser mayor que la tarifa.
select viaje_id, tarifa, propina
from {{ ref('fct_viajes') }}
where propina > tarifa
