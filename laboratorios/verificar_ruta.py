"""Verifica la ruta en español sin ejecutar los laboratorios.

Revisa:
  1. Enlaces internos de README.md, docs/es/*.md, laboratorios/**/README.md y los mapas LEEME.md
     (que el archivo exista y, si hay #ancla, que el título exista).
  2. Enlaces al repositorio original fijados al commit de referencia: que la ruta exista en ese commit
     (requiere el remoto "upstream" o tener ese commit en el historial local).
  3. Configuración: `docker compose config` de cada docker-compose.yml, que los YAML se puedan leer
     y que los .py compilen.

Uso, desde la raíz del repositorio:
    uv run --no-project --with pyyaml python laboratorios/verificar_ruta.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
REF = "a66ad5da2598d7ac147b37eec29632c93f4b1d9d"
UPSTREAM = re.compile(
    r"https://github\.com/DataTalksClub/data-engineering-zoomcamp/(?:blob|tree)/" + REF + r"/([^)\s#?]+)"
)
ENLACE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
IGNORAR = {".venv", "node_modules", "target", "datos", "salida", ".dlt_pipelines", "dbt_packages"}


def slug(titulo: str) -> str:
    """Convierte un título Markdown en el ancla que genera GitHub."""
    t = titulo.strip().lower()
    t = re.sub(r"[`*_~]", "", t)
    t = "".join(c for c in t if unicodedata.category(c)[0] in "LN" or c in " -")
    return t.replace(" ", "-")


def anclas(archivo: Path) -> set[str]:
    vistos: dict[str, int] = {}
    resultado = set()
    en_codigo = False
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
        if en_codigo:
            continue
        m = re.match(r"^#{1,6}\s+(.*)", linea)
        if m:
            s = slug(m.group(1))
            n = vistos.get(s, 0)
            resultado.add(s if n == 0 else f"{s}-{n}")
            vistos[s] = n + 1
    return resultado


def documentos() -> list[Path]:
    docs = [RAIZ / "README.md", *sorted((RAIZ / "docs" / "es").glob("*.md"))]
    for p in sorted((RAIZ / "laboratorios").rglob("README.md")):
        if not IGNORAR.intersection(p.relative_to(RAIZ).parts):
            docs.append(p)
    for p in sorted(RAIZ.rglob("LEEME.md")):
        if not IGNORAR.intersection(p.relative_to(RAIZ).parts):
            docs.append(p)
    return docs


def rutas_upstream() -> set[str] | None:
    r = subprocess.run(["git", "ls-tree", "-r", "-t", "--name-only", REF], cwd=RAIZ, capture_output=True, text=True)
    return set(r.stdout.split()) if r.returncode == 0 else None


def main() -> int:
    errores: list[str] = []
    avisos: list[str] = []
    upstream = rutas_upstream()
    if upstream is None:
        avisos.append(f"No encontré el commit {REF[:7]}: ejecuta 'git fetch upstream' para validar los enlaces al original.")

    n_internos = n_upstream = 0
    for doc in documentos():
        texto = doc.read_text(encoding="utf-8")
        texto_sin_codigo = re.sub(r"```.*?```", "", texto, flags=re.S)
        for destino in ENLACE.findall(texto_sin_codigo):
            rel = doc.relative_to(RAIZ)
            m = UPSTREAM.match(destino)
            if m and upstream is not None:
                n_upstream += 1
                if m.group(1).rstrip("/") not in upstream:
                    errores.append(f"{rel}: '{m.group(1)}' no existe en el commit de referencia")
                continue
            if re.match(r"^[a-z]+:", destino):
                continue  # enlace externo
            n_internos += 1
            ruta, _, ancla = destino.partition("#")
            objetivo = (doc.parent / ruta).resolve() if ruta else doc
            if not objetivo.exists():
                errores.append(f"{rel}: enlace roto -> {destino}")
            elif ancla and objetivo.suffix == ".md" and ancla not in anclas(objetivo):
                errores.append(f"{rel}: ancla inexistente -> {destino}")

    # Configuración
    composes = sorted(p for p in (RAIZ / "laboratorios").rglob("docker-compose.y*ml") if not IGNORAR.intersection(p.parts))
    for c in composes:
        r = subprocess.run(["docker", "compose", "-f", str(c), "config", "-q"], capture_output=True, text=True)
        if r.returncode != 0:
            errores.append(f"{c.relative_to(RAIZ)}: docker compose config falló: {r.stderr.strip()[:200]}")
    yamls = [
        p
        for p in (RAIZ / "laboratorios").rglob("*.y*ml")
        if not IGNORAR.intersection(p.parts) and p.name not in ("uv.lock",)
    ]
    for y in yamls:
        try:
            yaml.safe_load(y.read_text(encoding="utf-8")) if "{%" not in y.read_text(encoding="utf-8") else None
        except yaml.YAMLError as exc:
            errores.append(f"{y.relative_to(RAIZ)}: YAML inválido: {str(exc)[:120]}")
    pys = [p for p in (RAIZ / "laboratorios").rglob("*.py") if not IGNORAR.intersection(p.parts)]
    for p in pys:
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except SyntaxError as exc:
            errores.append(f"{p.relative_to(RAIZ)}: no compila: {exc}")

    print(f"Documentos revisados       : {len(documentos())}")
    print(f"Enlaces internos           : {n_internos}")
    print(f"Enlaces al original ({REF[:7]}): {n_upstream}")
    print(f"docker-compose validados   : {len(composes)}")
    print(f"YAML leídos                : {len(yamls)}")
    print(f"Archivos Python compilados : {len(pys)}")
    for a in avisos:
        print("AVISO:", a)
    for e in errores:
        print("ERROR:", e)
    print("\nRUTA OK ✅" if not errores else f"\n{len(errores)} error(es)")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
