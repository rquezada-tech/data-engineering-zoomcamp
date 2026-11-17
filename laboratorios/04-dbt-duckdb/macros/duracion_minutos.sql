{#
  Macro = una "función" reutilizable de SQL.
  Calcula los minutos entre dos marcas de tiempo, con un decimal.
  Uso en un modelo:  {{ duracion_minutos('inicio', 'fin') }}
#}
{% macro duracion_minutos(columna_inicio, columna_fin) %}
    round(date_diff('second', {{ columna_inicio }}, {{ columna_fin }}) / 60.0, 1)
{% endmacro %}
