-- Capa intermedia: aplicamos reglas de negocio.
-- Regla: un viaje con tarifa 0 no es un viaje cobrable, así que lo dejamos fuera.
select
    v.*,
    p.descripcion as tipo_pago
from {{ ref('stg_viajes') }} as v
left join {{ ref('tipos_pago') }} as p
    on v.tipo_pago_id = p.tipo_pago_id
where v.tarifa > 0
