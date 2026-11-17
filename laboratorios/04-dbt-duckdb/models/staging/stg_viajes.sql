-- Capa staging: limpiamos nombres y tipos. Una fila por viaje, sin filtrar nada todavía.
select
    viaje_id,
    inicio,
    fin,
    {{ duracion_minutos('inicio', 'fin') }} as duracion_min,
    zona_origen,
    zona_destino,
    cast(distancia_km as decimal(8, 2)) as distancia_km,
    cast(tarifa as decimal(10, 2)) as tarifa,
    cast(propina as decimal(10, 2)) as propina,
    tipo_pago as tipo_pago_id
from {{ source('crudo', 'viajes') }}
