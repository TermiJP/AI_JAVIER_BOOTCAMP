"""Comprobaciones — SOLUTION (estructura + /health opcional, sin Gemini en /ask)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def _revisar_estatico() -> list[str]:
    fallos: list[str] = []

    schemas = _leer(ROOT / "schemas.py")
    if "min_length=1" not in schemas:
        fallos.append("schemas.py: AskIn.pregunta debe tener min_length=1")

    models = _leer(ROOT / "src" / "models.py")
    if "created_at" not in models or "foreign_key" not in models:
        fallos.append("models.py: Conversation/Message incompletos")

    db_src = _leer(ROOT / "src" / "db.py")
    bloque_save = (
        db_src.split("def save_turn")[1].split("def ")[0]
        if "def save_turn" in db_src
        else ""
    )
    if "NotImplementedError" in bloque_save or "session.add" not in bloque_save:
        fallos.append("db.py: save_turn incompleto")

    app_src = _leer(ROOT / "app.py")
    bloque_ask = (
        app_src.split("def ask")[1].split("@app.post")[0] if "def ask" in app_src else ""
    )
    if "NotImplementedError" in bloque_ask:
        fallos.append("app.py: POST /ask no debe tener NotImplementedError")
    if "procesar_turno" not in bloque_ask:
        fallos.append("app.py: /ask debe llamar procesar_turno")
    if "save_turn" not in app_src and "_persistir_si_hay_respuesta" not in bloque_ask:
        fallos.append("app.py: falta persistencia del turno")

    bloque_msgs = (
        app_src.split("def get_messages")[1] if "def get_messages" in app_src else ""
    )
    if "NotImplementedError" in bloque_msgs or "list_messages" not in bloque_msgs:
        fallos.append("app.py: GET messages debe usar list_messages")

    return fallos


def _check_health() -> list[str]:
    fallos: list[str] = []
    try:
        import os

        os.environ.setdefault("GEMINI_API_KEY", "verificar-dummy")

        from fastapi.testclient import TestClient

        from app import app
    except Exception as exc:  # noqa: BLE001
        return [f"No se pudo importar la app: {exc}"]

    client = TestClient(app)
    r = client.get("/health")
    if r.status_code != 200 or r.json().get("status") != "ok":
        fallos.append(f"/health falló: {r.status_code} {r.text}")
    if r.json().get("storage") != "sqlite":
        fallos.append('/health debe incluir "storage": "sqlite"')
    return fallos


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    fallos = _revisar_estatico()
    if args.check:
        fallos.extend(_check_health())

    if fallos:
        print("Pendiente:")
        for f in fallos:
            print(f"  - {f}")
        return 1

    print("OK: checks estructurales" + (" y /health" if args.check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
