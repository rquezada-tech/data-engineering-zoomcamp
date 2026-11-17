-- Tabla donde Flink escribe el resumen por minuto de cada sensor.
-- La clave primaria permite "upsert": si llega una versión nueva de la misma ventana, se actualiza.
CREATE TABLE IF NOT EXISTS lecturas_por_minuto (
    ventana_inicio  TIMESTAMP        NOT NULL,
    ventana_fin     TIMESTAMP        NOT NULL,
    sensor_id       VARCHAR(20)      NOT NULL,
    lecturas        BIGINT           NOT NULL,
    temp_promedio   DOUBLE PRECISION NOT NULL,
    temp_maxima     DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (ventana_inicio, sensor_id)
);
