"""
Rate limit en memoria: máximo N peticiones por API key cada 60 segundos.
"""

import logging
import time
from collections import defaultdict, deque

from fastapi import HTTPException

import config

logger = logging.getLogger(__name__)

_hits: dict[str, deque[float]] = defaultdict(deque)


def check_rate_limit(api_key: str) -> None:
    """Si esta clave supera RATE_LIMIT_PER_MINUTE en 60 s → 429."""
    # TODO 2: ventana 60 s con time.monotonic(); limpiar hits viejos en q
    # TODO 2: si len(q) >= config.RATE_LIMIT_PER_MINUTE → HTTPException 429
    # TODO 2: si no, registrar este hit (q.append(now))
    raise NotImplementedError("TODO 2: completar check_rate_limit")
