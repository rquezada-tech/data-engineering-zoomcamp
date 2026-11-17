-- Tabla de hechos: una fila por viaje válido, con llaves hacia las dimensiones.
select
    v.viaje_id,
    v.inicio,
    v.fin,
    v.duracion_min,
    zo.zona_id as zona_origen_id,
    zd.zona_id as zona_destino_id,
    v.distancia_km,
    v.tarifa,
    v.propina,
    v.tarifa + v.propina as total_cobrado,
    v.tipo_pago
from {{ ref('int_viajes_validos') }} as v
left join {{ ref('dim_zonas') }} as zo on v.zona_origen = zo.zona
left join {{ ref('dim_zonas') }} as zd on v.zona_destino = zd.zona
