-- Dimensión: describe "dónde". Una fila por zona.
select
    zona_id,
    zona,
    tipo_zona
from {{ ref('zonas') }}
