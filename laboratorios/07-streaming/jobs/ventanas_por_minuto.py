"""Trabajo de PyFlink: promedio de temperatura por sensor en ventanas de 1 minuto.

Flujo:  Redpanda (tópico lecturas-sensores)  ->  Flink (TUMBLE de 1 min)  ->  PostgreSQL

Se envía al clúster con:
  docker compose exec jobmanager ./bin/flink run -py /opt/jobs/ventanas_por_minuto.py -d
"""
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10_000)  # guarda su progreso cada 10 s
    t_env = StreamTableEnvironment.create(env, environment_settings=EnvironmentSettings.in_streaming_mode())

    # 1) FUENTE: el tópico de Redpanda, leído como si fuera una tabla.
    t_env.execute_sql(
        """
        CREATE TABLE lecturas (
            sensor_id   STRING,
            temperatura DOUBLE,
            ts          BIGINT,
            -- Convertimos los milisegundos en una fecha-hora de evento...
            evento_ts   AS TO_TIMESTAMP_LTZ(ts, 3),
            -- ...y declaramos la marca de agua: aceptamos eventos hasta 5 s atrasados.
            WATERMARK FOR evento_ts AS evento_ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'lecturas-sensores',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-ventanas',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
        """
    )

    # 2) DESTINO: la tabla de PostgreSQL (con clave primaria -> upsert).
    t_env.execute_sql(
        """
        CREATE TABLE lecturas_por_minuto (
            ventana_inicio TIMESTAMP(3),
            ventana_fin    TIMESTAMP(3),
            sensor_id      STRING,
            lecturas       BIGINT,
            temp_promedio  DOUBLE,
            temp_maxima    DOUBLE,
            PRIMARY KEY (ventana_inicio, sensor_id) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/streaming',
            'table-name' = 'lecturas_por_minuto',
            'username' = 'postgres',
            'password' = 'postgres'
        )
        """
    )

    # 3) LA TRANSFORMACIÓN: ventanas fijas (TUMBLE) de 1 minuto por sensor.
    t_env.execute_sql(
        """
        INSERT INTO lecturas_por_minuto
        SELECT
            window_start,
            window_end,
            sensor_id,
            COUNT(*)          AS lecturas,
            AVG(temperatura)  AS temp_promedio,
            MAX(temperatura)  AS temp_maxima
        FROM TABLE(
            TUMBLE(TABLE lecturas, DESCRIPTOR(evento_ts), INTERVAL '1' MINUTE)
        )
        WHERE sensor_id <> 'cierre'
        GROUP BY window_start, window_end, sensor_id
        """
    )


if __name__ == "__main__":
    main()
