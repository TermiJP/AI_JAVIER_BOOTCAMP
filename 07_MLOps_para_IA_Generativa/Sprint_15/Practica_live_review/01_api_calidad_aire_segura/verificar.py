"""Comprobaciones — TODOs de seguridad/observabilidad (alumno)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def _revisar_estatico() -> list[str]:
    fallos: list[str] = []

    sec = _leer(ROOT / "security.py")
    if "NotImplementedError" in sec or "TODO 1" in sec:
        fallos.append("TODO 1: completar require_api_key en security.py")

    rl = _leer(ROOT / "rate_limit.py")
    if "NotImplementedError" in rl or "TODO 2" in rl:
        fallos.append("TODO 2: completar check_rate_limit en rate_limit.py")

    app_src = _leer(ROOT / "app.py")
    if "CORSMiddleware" not in app_src or "TODO 3" in app_src:
        fallos.append("TODO 3: añadir CORSMiddleware con config.CORS_ORIGINS en app.py")

    bloque_ask = app_src.split("def ask")[1].split("@app.post")[0] if "def ask" in app_src else ""
    if "duration_ms" not in bloque_ask or "TODO 4" in bloque_ask:
        fallos.append("TODO 4: logs thread_id + duration_ms en POST /ask")

    if "ThreadPoolExecutor" not in app_src or "TODO 5" in bloque_ask:
        fallos.append("TODO 5: timeout ASK_TIMEOUT_SECONDS → 504 en POST /ask")

    return fallos


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="(opcional) import + /health")
    args = parser.parse_args()

    fallos = _revisar_estatico()
    if args.check and not fallos:
        try:
            import os

            os.environ.setdefault("GEMINI_API_KEY", "verificar-dummy")
            os.environ.setdefault("API_KEY", "verificar-dummy")
            from fastapi.testclient import TestClient

            from app import app

            client = TestClient(app)
            r = client.get("/health")
            if r.status_code != 200:
                fallos.append(f"/health: {r.status_code}")
        except Exception as exc:  # noqa: BLE001
            fallos.append(f"Import/app: {exc}")

    if fallos:
        print("Pendiente:")
        for f in fallos:
            print(f"  - {f}")
        return 1

    print("OK: TODOs de seguridad completados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
