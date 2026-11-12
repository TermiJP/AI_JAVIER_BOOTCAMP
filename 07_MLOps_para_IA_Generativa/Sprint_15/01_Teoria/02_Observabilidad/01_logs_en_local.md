![Cabecera](../../assets/cabecera_mlops.png)

# Logs en local

En local basta con **logging** bien hecho: qué pasó, a qué conversación pertenece y cuánto tardó. No hace falta un sistema de métricas aparte.

## Logging

Usamos el módulo `logging` de Python (no solo `print`). El resultado lo vemos en la consola de uvicorn.

```python
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger.info("GET /items status=%s duration_ms=%s", status, duration_ms)
logger.error("fallo en /ask: %s", exc)
```

### Qué logueamos

- Método, path, status HTTP y duración (`duration_ms`).
- `thread_id` cuando hay conversación.
- Tipo de error o mensaje genérico (sin stack al cliente; el detalle puede ir al log).

### Qué no logueamos

- Secretos: `API_KEY`, `GEMINI_API_KEY`, contraseñas, connection strings.
- Bodies enteros con datos personales si no hacen falta para depurar.

### Niveles útiles

- `INFO` — request normal.
- `WARNING` — 401/429 repetidos.
- `ERROR` — fallos 5xx, timeouts.

## Correlación: `thread_id`

En APIs de agente ya tenemos **`thread_id`** (conversación). Sirve también para **seguir** el rastro en logs.

```text
2026-… INFO POST /ask thread_id=demo-1 status=200 duration_ms=4200
2026-… INFO tool rag_guia ok thread_id=demo-1
```

Sin id de correlación, tres líneas de log de tres usuarios se mezclan. En el agente logueamos siempre el `thread_id` del body en `/ask` y `/approve`.

### `request_id` (opcional)

Un UUID por petición HTTP ayuda si el mismo hilo tiene varias llamadas. Podemos generarlo en un middleware o reutilizar `thread_id` cuando baste para la demo.

## Latencia y errores con el mismo log

No hace falta Prometheus. Con el log ya medimos:

| Señal | Cómo |
|-------|------|
| Latencia | `duration_ms` al final de la request |
| Errores | Contar 401 / 429 / 5xx a ojo en consola |
| Coste tokens | Log opcional si el LLM devuelve usage |

```python
import time

t0 = time.perf_counter()
# ... manejar request ...
duration_ms = int((time.perf_counter() - t0) * 1000)
logger.info("... duration_ms=%s", duration_ms)
```

En GenAI, latencias de **segundos** son normales. Lo raro es un `/ask` de 120 s sin timeout.

## Resumen

- Formato estable + secrets fuera del log.
- `thread_id` para no mezclar conversaciones.
- Latencia + status en el log = métrica mínima; paneles → más adelante / PaaS.
