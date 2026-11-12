"""Configuración — agente calidad del aire + SQLite + seguridad/observabilidad."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

DATABASE_URL = f"sqlite:///{ROOT / 'historial.db'}"

GEMINI_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 2
MAX_TURNS_DEFAULT = 4
MAX_ITER = 8

MADRID_AIRE_URL = (
    "https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/"
    "calair_tiemporeal.json?pageSize=50"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_calidad_aire.txt"
AIRE_FALLBACK_PATH = DATA_DIR / "aire_fallback.json"

IMAGEN_DEFAULT_PATH = ASSETS_DIR / "imagen_demo.jpg"

MAGNITUDES = {
    "1": "SO2",
    "6": "CO",
    "7": "NO",
    "8": "NO2",
    "9": "PM2.5",
    "10": "PM10",
    "12": "NOx",
    "14": "O3",
    "20": "TOL",
    "30": "BEN",
    "42": "TCH",
    "44": "CH4",
}

DEMO_MENSAJES = [
    (
        "Zona centro, contaminante NO2. Consulta la guía y datos de la API "
        "de Madrid. Propón un plan breve de qué hacer / cómo interpretar."
    ),
]

# --- Seguridad (API key, rate limit, CORS, timeout) -----------------------

API_KEY: str | None = os.getenv("API_KEY") or None
RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))

_cors_raw = os.getenv(
    "CORS_ORIGINS",
    "http://127.0.0.1:8501,http://localhost:8501,http://127.0.0.1:8000,http://localhost:8000",
)
CORS_ORIGINS: list[str] = [o.strip() for o in _cors_raw.split(",") if o.strip()]

ASK_TIMEOUT_SECONDS: int = int(os.getenv("ASK_TIMEOUT_SECONDS", "300"))
