# Imagen de la ingesta: Python + las librerías que necesita el script.
FROM python:3.13-slim

# uv instala dependencias de Python mucho más rápido que pip.
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml

COPY ingesta.py .
ENTRYPOINT ["python", "ingesta.py"]
