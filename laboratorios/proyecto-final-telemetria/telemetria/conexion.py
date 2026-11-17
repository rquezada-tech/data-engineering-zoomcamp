"""Conexión segura a LocalCloud (adaptada de laboratorios/03-bigquery-parquet/lab/comun.py).

Este archivo hace tres cosas:

1. Crea los clientes de BigQuery y Cloud Storage apuntando SIEMPRE a LocalCloud.
2. Bloquea cualquier intento de conectarse a Google Cloud real. Si algo falla,
   el pipeline se detiene con un mensaje claro en vez de "probar suerte"
   contra internet.
"""

from __future__ import annotations

import os
import socket
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

PROYECTO_POR_DEFECTO = "local-gcp-project"  # proyecto que LocalCloud crea solo

# Hosts permitidos: solo tu propio computador.
HOSTS_LOCALES = {"localhost", "127.0.0.1", "::1"}
# Dominios que el proyecto jamás debe tocar.
DOMINIOS_PROHIBIDOS = ("googleapis.com", "google.com", "googleusercontent.com", "gcr.io", "pkg.dev")


class ErrorLaboratorio(RuntimeError):
    """Error con un mensaje pensado para la persona que ejecuta el proyecto."""


def detener(mensaje: str) -> None:
    """Muestra un mensaje claro y termina con código 2."""
    print("\n" + "=" * 70, file=sys.stderr)
    print("EL PIPELINE SE DETUVO", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(mensaje.strip(), file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Bloqueo de red: nada de Google Cloud real
# --------------------------------------------------------------------------
_getaddrinfo_original = socket.getaddrinfo


def _getaddrinfo_protegido(host, *args, **kwargs):
    nombre = (host.decode() if isinstance(host, bytes) else str(host or "")).lower().rstrip(".")
    if any(nombre == d or nombre.endswith("." + d) for d in DOMINIOS_PROHIBIDOS):
        raise ErrorLaboratorio(
            f"Se intentó conectar a '{nombre}', que es Google Cloud real. "
            "Este proyecto solo trabaja con LocalCloud en tu computador, así que la conexión se bloqueó."
        )
    return _getaddrinfo_original(host, *args, **kwargs)


def bloquear_google_cloud() -> None:
    """Hace que cualquier conexión a *.googleapis.com (u otros dominios de Google) falle al instante."""
    socket.getaddrinfo = _getaddrinfo_protegido
    # Evita que las librerías de Google intenten leer credenciales reales del equipo.
    for variable in ("GOOGLE_APPLICATION_CREDENTIALS", "CLOUDSDK_CONFIG"):
        os.environ.pop(variable, None)


# --------------------------------------------------------------------------
# Endpoints locales
# --------------------------------------------------------------------------
def _endpoint(variable: str, por_defecto: str) -> str:
    valor = os.environ.get(variable, "").strip() or por_defecto
    if "://" not in valor:
        valor = "http://" + valor
    url = urlparse(valor)
    if (url.hostname or "").lower() not in HOSTS_LOCALES:
        detener(
            f"""
La variable {variable} vale '{valor}', que NO es una dirección de tu computador.

Este proyecto solo se conecta a LocalCloud en localhost para no tocar Google Cloud real.
Arréglalo así:

    unset {variable}
    eval "$(curl -fsS 'http://localhost:5380/env?format=shell')"
"""
        )
    return valor.rstrip("/")


def configuracion() -> dict[str, str]:
    return {
        "proyecto": os.environ.get("GOOGLE_CLOUD_PROJECT", "").strip() or PROYECTO_POR_DEFECTO,
        "gateway": _endpoint("LOCALCLOUD_GATEWAY", "http://localhost:5380"),
        "bigquery": _endpoint("BIGQUERY_EMULATOR_HOST", "http://localhost:5388"),
        "storage": _endpoint("STORAGE_EMULATOR_HOST", "http://localhost:5382"),
    }


def verificar_localcloud(cfg: dict[str, str]) -> None:
    """Comprueba que LocalCloud esté encendido antes de hacer cualquier cosa."""
    url = cfg["gateway"] + "/readiness"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            if resp.status != 200:
                raise urllib.error.URLError(f"respuesta HTTP {resp.status}")
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as exc:
        detener(
            f"""
No pude hablar con LocalCloud en {url}
Detalle técnico: {exc}

Lo más probable es que el emulador no esté encendido. Desde la raíz del repositorio ejecuta:

    docker compose -f laboratorios/localcloud/docker-compose.yml up -d --wait

y vuelve a intentar. Si Docker Desktop no está abierto, ábrelo primero.

(El proyecto NO intentará usar Google Cloud real como alternativa.)
"""
        )


def clientes():
    """Devuelve (bigquery.Client, storage.Client) conectados a LocalCloud."""
    bloquear_google_cloud()
    cfg = configuracion()
    verificar_localcloud(cfg)

    # Importamos aquí para que los mensajes de arriba aparezcan incluso si falta una librería.
    try:
        from google.auth.credentials import AnonymousCredentials
        from google.cloud import bigquery, storage
    except ImportError as exc:
        detener(
            f"""
Falta una librería de Python ({exc}).
Instala las dependencias del proyecto con:

    cd laboratorios/proyecto-final-telemetria
    uv sync
"""
        )

    # STORAGE_EMULATOR_HOST le dice a la librería de Storage que use el emulador.
    os.environ["STORAGE_EMULATOR_HOST"] = cfg["storage"]

    credenciales = AnonymousCredentials()  # sin usuario ni contraseña: el emulador no las necesita
    bq = bigquery.Client(
        project=cfg["proyecto"],
        credentials=credenciales,
        client_options={"api_endpoint": cfg["bigquery"]},
    )
    gcs = storage.Client(
        project=cfg["proyecto"],
        credentials=credenciales,
        client_options={"api_endpoint": cfg["storage"]},
    )

    # Doble chequeo: si por cualquier motivo el cliente quedó apuntando a Google, paramos.
    for nombre, cliente, esperado in (("BigQuery", bq, cfg["bigquery"]), ("Cloud Storage", gcs, cfg["storage"])):
        base = cliente._connection.API_BASE_URL.rstrip("/")
        if base != esperado:
            detener(f"El cliente de {nombre} apunta a {base} en vez de {esperado}. Se cancela por seguridad.")
    return bq, gcs


def titulo(texto: str) -> None:
    print("\n" + texto)
    print("-" * len(texto))


def ejecutar(fn) -> None:
    """Ejecuta un paso y traduce los errores a mensajes entendibles."""
    try:
        fn()
    except ErrorLaboratorio as exc:
        detener(str(exc))
    except Exception as exc:  # noqa: BLE001 - queremos un mensaje claro para cualquier error
        texto = str(exc)
        if "Connection refused" in texto or "Max retries exceeded" in texto:
            detener(
                f"""
LocalCloud dejó de responder a mitad del paso.
Detalle técnico: {texto[:400]}

Revisa que el contenedor siga encendido:

    docker compose -f laboratorios/localcloud/docker-compose.yml ps
"""
            )
        raise
