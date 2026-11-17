{#
  Por defecto dbt nombra los schemas como "<schema del perfil>_<schema del modelo>" (ej: main_staging).
  Este ajuste deja solo el nombre del modelo (staging, marts, ...), que es más fácil de leer.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}{{ target.schema }}{%- else -%}{{ custom_schema_name | trim }}{%- endif -%}
{%- endmacro %}
