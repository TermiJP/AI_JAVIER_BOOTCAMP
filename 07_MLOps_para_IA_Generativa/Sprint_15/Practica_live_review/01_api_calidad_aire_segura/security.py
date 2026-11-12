"""
Capa de seguridad: comprobar API key y, si es válida, aplicar rate limit.

FastAPI llama a `require_api_key` vía Depends(...) ANTES de entrar a la ruta.
"""

import logging

from fastapi import HTTPException, Query

import config
from rate_limit import check_rate_limit

logger = logging.getLogger(__name__)


def require_api_key(
    api_key: str | None = Query(
        default=None,
        description="Clave de acceso (misma que API_KEY en .env)",
    ),
) -> str:
    """
    1) Servidor sin API_KEY en .env → 503 (mal configurado).
    2) Cliente sin clave o clave distinta → 401.
    3) Clave OK → rate limit; si pasa, devolvemos la clave (el endpoint sigue).
    """
    # TODO 1: si config.API_KEY falta → HTTPException 503 (sin loguear secretos)
    # TODO 1: si api_key ausente o distinta de config.API_KEY → HTTPException 401
    # TODO 1: si la clave es válida → check_rate_limit(api_key) y return api_key
    raise NotImplementedError("TODO 1: completar require_api_key")
