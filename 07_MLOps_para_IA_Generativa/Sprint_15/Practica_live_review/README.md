# Live Review — Calidad del aire segura

Práctica: **mismo agente LangGraph de calidad del aire** e historial SQLite que en el sprint anterior, ahora con **API key**, **rate limit**, **CORS**, **logs** (`thread_id`, `duration_ms`) y **timeout** → 504. Todo en **local** (sin deploy).

| Carpeta | Rol |
|---------|-----|
| [`01_api_calidad_aire_segura/`](01_api_calidad_aire_segura/) | Alumno — **5 TODOs** (seguridad + app) |
| [`01_api_calidad_aire_segura_SOLUTION/`](01_api_calidad_aire_segura_SOLUTION/) | Referencia profesor |
| [`02_cliente_streamlit/`](02_cliente_streamlit/) | Cliente Streamlit **dado** |

## Qué se da / qué se pide

| Dado | Pedido (alumno) |
|------|------------------|
| Agente completo (`src/`, `data/`, schemas, `db`, `/ask` de negocio) | **1–2** `security.py` + `rate_limit.py` |
| `config.py` con variables de seguridad | **3–5** CORS, logs y timeout en `app.py` |
| `Depends(require_api_key)` ya en rutas sensibles | |
| Cliente Streamlit | Usarlo para probar 401/200/429 |

## Flujo

```text
Streamlit (.env API_KEY) → POST /ask?api_key=... → agente + SQLite
GET /health (público)
```

Detalle de TODOs y práctica guiada 401/429/504: README de cada carpeta API y `verificar.py`.
