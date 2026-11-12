![Cabecera](../../assets/cabecera_mlops.png)

# Rate, timeouts y errores

Aunque tengamos API key, hace falta limitar **cuántas** peticiones entran y **cuánto** puede durar un trabajo. Python decide esos topes; el cliente recibe códigos HTTP claros.

## Rate limiting

Un cliente (o un bucle mal escrito) puede **lanzar muchas peticiones**: coste de LLM, CPU, DoS accidental.

- Contamos peticiones **por API key** en una ventana de tiempo (p. ej. 1 minuto).
- Si se supera el límite → **429 Too Many Requests**.
- En memoria (dict / `deque`) vale para demo; en producción usaríamos Redis u otro almacén compartido entre procesos.

```text
misma API_KEY · 30 req/min  →  OK
misma API_KEY · 31ª en ese min  →  429 Too Many Requests
```

### Ejemplo en Python

Ventana deslizante de 60 s: timestamps por API key; si hay demasiados → **429**.

```python
import time
from collections import defaultdict, deque

from fastapi import HTTPException

_hits: dict[str, deque[float]] = defaultdict(deque)

RATE_LIMIT_PER_MINUTE = 30
WINDOW_SECONDS = 60.0


def check_rate_limit(api_key: str) -> None:
    now = time.monotonic()
    q = _hits[api_key]

    while q and (now - q[0]) > WINDOW_SECONDS:
        q.popleft()

    if len(q) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Demasiadas peticiones; reintentar en un minuto",
        )

    q.append(now)
```

Lo llamamos **después** de validar la API key. El límite (`RATE_LIMIT_PER_MINUTE`) suele vivir en el `.env`.

### Importante

- No sustituye la API key.
- No es un WAF ni Cloud Armor.
- El contador en RAM se **reinicia** al reiniciar `uvicorn`. Si quisiéramos persistencia / varios procesos → Redis.

En práctica bajamos el límite a propósito para forzar el **429**.

## Timeouts

Una llamada externa (LLM, HTTP, tool) no puede colgar el proceso para siempre. Tope en config — `ASK_TIMEOUT_SECONDS` — y si se pasa → **504**; el traceback solo en logs.

| Pieza | Ejemplo |
|-------|---------|
| Config | `ASK_TIMEOUT_SECONDS=300` (margen) o `15` para forzar |
| Si se pasa | **504** con mensaje claro |
| Detalle | Solo en **logs** |

En el CRUD el foco suele ser API key y rate limit. El timeout hands-on encaja cuando hay una llamada real lenta (LLM / agente).

### Ejemplo en Python

```python
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError

from fastapi import HTTPException

ASK_TIMEOUT_SECONDS = 300


def con_timeout(fn, *args):
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(fn, *args)
        return future.result(timeout=ASK_TIMEOUT_SECONDS)


try:
    out = con_timeout(procesar_turno, ...)
except FuturesTimeoutError:
    raise HTTPException(
        status_code=504,
        detail="El turno del agente superó el tiempo máximo",
    ) from None
```

**Nota:** a los N segundos la API **decide** el 504. El cliente puede recibirlo un poco después si el LLM/SDK sigue en el hilo de fondo. Lo que cuenta: status **504** + log del límite.

## Errores al cliente

| Código | Cuándo |
|--------|--------|
| **401** | API key ausente o incorrecta |
| **429** | Rate limit |
| **422** | Body inválido (Pydantic) |
| **503** | Falta configuración (`API_KEY` no definida) |
| **504** | Timeout de trabajo |
| **500** | Error inesperado; mensaje genérico al cliente |

Nunca devolvemos secretos ni stack traces en el JSON público.

## Límites de ejecución

Además del timeout:

- Tamaño / forma del body → Pydantic (**422** si no encaja).
- `max_turns` u otros topes del agente → en código, no “confiar en el prompt”.

Misma filosofía que en S14: **límites en Python**.

## Resumen

- Rate limit → **429**; timeout (`ASK_TIMEOUT_SECONDS`) → **504**.
- Códigos claros al cliente; detalle en logs.
- Python decide los guardrails.
