-- Reporte: lo que miraría un dashboard. Ingresos por mes y por zona de origen.
select
    date_trunc('month', f.inicio)::date as mes,
    z.zona,
    z.tipo_zona,
    count(*) as viajes,
    sum(f.tarifa) as ingresos_tarifa,
    sum(f.propina) as ingresos_propina,
    sum(f.total_cobrado) as ingresos_totales,
    round(avg(f.distancia_km), 2) as distancia_promedio_km
from {{ ref('fct_viajes') }} as f
join {{ ref('dim_zonas') }} as z on f.zona_origen_id = z.zona_id
group by all
order by mes, ingresos_totales desc
