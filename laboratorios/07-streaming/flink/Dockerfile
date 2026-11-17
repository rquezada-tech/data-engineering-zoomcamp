# Imagen de Flink con Python (PyFlink) y conectores para Kafka/Redpanda y PostgreSQL.
# Funciona en Apple Silicon (arm64) y en Intel/AMD (amd64).
FROM flink:2.2.0-scala_2.12-java17

USER root

# Python 3.12 (Ubuntu 24.04) + herramientas para compilar "pemja", una dependencia de PyFlink
# que no publica paquete precompilado para arm64 y necesita un JDK completo (con cabeceras C).
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-dev build-essential openjdk-17-jdk-headless wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Entorno virtual con PyFlink. JAVA_HOME apunta al JDK solo durante la instalación.
RUN JDK_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")" \
    && python3 -m venv /opt/venv \
    && JAVA_HOME="$JDK_HOME" /opt/venv/bin/pip install --no-cache-dir "apache-flink==2.2.0" \
    && ln -sf /opt/venv/bin/python /usr/local/bin/python

# Conectores (archivos .jar) que Flink carga al arrancar. flink-json ya viene en la imagen base.
WORKDIR /opt/flink/lib
RUN wget -q https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/4.0.1-2.0/flink-sql-connector-kafka-4.0.1-2.0.jar \
    && wget -q https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc-core/4.0.0-2.0/flink-connector-jdbc-core-4.0.0-2.0.jar \
    && wget -q https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc-postgres/4.0.0-2.0/flink-connector-jdbc-postgres-4.0.0-2.0.jar \
    && wget -q https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.10/postgresql-42.7.10.jar \
    && chown -R flink:flink /opt/flink/lib

WORKDIR /opt/flink
USER flink
