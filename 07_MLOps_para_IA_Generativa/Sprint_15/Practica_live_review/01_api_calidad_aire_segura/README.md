# Live Review — API agente calidad del aire segura

Seguimos con el **mismo agente de calidad del aire** e historial SQLite. El grafo y las tools vienen **dados**. Nos centramos en **seguridad y observabilidad** en local: API key, rate limit, CORS, logs con `thread_id` + `duration_ms`, timeout por turno.

```text
cliente → /ask?api_key=... → rate limit → procesar_turno (con timeout)
                ↓
        logs: thread_id + duration_ms
                ↓
        /health y /docs sin clave
```

**Requisitos:** Python 3.10+, `GEMINI_API_KEY` y `API_KEY` en `.env`.

`assets/imagen_demo.jpg` es la imagen demo de la tool `describir_imagen`.

---

## Estructura

```text
.
├── app.py             # Rutas + CORS + Depends + timeout + logs
├── security.py        # require_api_key (?api_key=)
├── rate_limit.py      # Contador en memoria → 429
├── config.py          # agente + API_KEY, rate limit, CORS, timeout
├── schemas.py
├── gemini_auth.py
├── src/               # agente + SQLModel (dado)
├── data/
├── assets/            # imagen_demo.jpg
├── verificar.py
└── README.md
```

Ejecutamos siempre **desde esta carpeta** (donde está `app.py`).

---

## TODOs (5)

Parte del proyecto (agente, historial, schemas, rutas de la API) viene **completo**. Completamos la capa segura:

| # | Dónde | Qué |
|---|--------|-----|
| **1** | `security.py` | Completar `require_api_key`: 503 si falta `API_KEY` en servidor, 401 si clave mala, luego `check_rate_limit` |
| **2** | `rate_limit.py` | Ventana 60 s, contador por clave → **429** |
| **3** | `app.py` | `CORSMiddleware` con `config.CORS_ORIGINS` |
| **4** | `app.py` | Tras `/ask`, log `INFO` con `thread_id` y `duration_ms` (sin secretos) |
| **5** | `app.py` | Envolver el turno con timeout (`ASK_TIMEOUT_SECONDS`) → **504** |

`Depends(require_api_key)` ya está en `/ask`, `/approve` y GET messages.

Orden sugerido: **1 → 2 → 3 → 4 → 5**.

---

## Instalación y arranque

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # GEMINI_API_KEY + API_KEY
uvicorn app:app --reload --port 8000
```

**http://127.0.0.1:8000/docs** — en rutas protegidas: *Try it out* → query **`api_key`** = valor del `.env`.

`GEMINI_API_KEY` ≠ `API_KEY`: la primera llama a Gemini; la segunda protege nuestra API.

Comprobar: `python verificar.py` (y `--check` cuando los TODOs estén hechos).

Cliente Streamlit (dado) para probar la API que habéis completado: [`../02_cliente_streamlit/`](../02_cliente_streamlit/).

---

## Rutas

| Método | Ruta | ¿`api_key`? | Qué hace |
|--------|------|-------------|----------|
| GET | `/health` | No | Pulso + `"storage": "sqlite"` |
| GET | `/docs` | No | Swagger |
| POST | `/ask` | **Sí** | Un turno; timeout → 504 |
| POST | `/approve` | **Sí** | HITL (dado; con `auto_aprobar` casi no lo usáis) |
| GET | `/threads/{thread_id}/messages` | **Sí** | Historial SQL |

---

## Práctica guiada

Sustituimos `<CLAVE>` por el valor de `API_KEY` en nuestro `.env`.  
Usad el mismo `thread_id` (p. ej. `demo-aire`) en los turnos que compartan historial.

> **Tiempo de `/ask`:** el agente llama a Gemini y a tools. **Cada `/ask` puede tardar ~1–3 minutos.** `/health` y `GET …/messages` son rápidos. Para el **429** preferimos `messages` (no gastamos cuota del LLM).

### 1) Health sin clave

GET `http://127.0.0.1:8000/health` → **200** `{"status":"ok", ...}`.

### 2) Ask sin API KEY → 401

POST `http://127.0.0.1:8000/ask` con body:

```json
{
  "pregunta": "Zona centro, contaminante NO2. Consulta la guía y datos de la API de Madrid. Propón un plan breve.",
  "thread_id": "demo-aire",
  "auto_aprobar": true
}
```

→ **401** (sin `?api_key=`).

En consola: `WARNING` de auth (sin imprimir la clave).

### 3) Ask con API KEY → 200 + logs

POST `http://127.0.0.1:8000/ask?api_key=<CLAVE>` con el **mismo body** → **200** y una `respuesta`.

En consola: `INFO POST /ask thread_id=demo-aire duration_ms=...` (**sin** secretos).

### 4) Historial con clave

GET `http://127.0.0.1:8000/threads/demo-aire/messages?api_key=<CLAVE>`  
→ mensajes `user` / `assistant` en SQLite.

GET sin `?api_key=` → **401**.

### 5) Rate limit → 429

Usamos GET messages (rápido) para no gastar Gemini.

1. En `.env`: `RATE_LIMIT_PER_MINUTE=5` y **reiniciamos** uvicorn (el `.env` no se recarga solo).
2. Repetimos GET `http://127.0.0.1:8000/threads/demo-aire/messages?api_key=<CLAVE>` **más de 5 veces** en menos de un minuto → **429**.

`/health` no cuenta (no pasa por `require_api_key`). Luego volved `RATE_LIMIT_PER_MINUTE` a un valor holgado (p. ej. **30**) y reiniciad.

### 6) Timeout — margen y forzar 504

`ASK_TIMEOUT_SECONDS` limita cuánto puede durar un turno. Si se pasa → **504**.

**Importante:** tras cambiar el `.env`, **reiniciamos uvicorn** (Ctrl+C y volver a lanzar).

**A) Uso normal (margen)**

1. Tras un `/ask` OK (paso 3), miramos `duration_ms` en consola.
2. En `.env`, `ASK_TIMEOUT_SECONDS` con margen (p. ej. **300**) y reiniciamos.

**B) Forzar un 504**

1. En `.env`: `ASK_TIMEOUT_SECONDS=15`.
2. Reiniciamos uvicorn.
3. POST `http://127.0.0.1:8000/ask?api_key=<CLAVE>` (mismo body que el paso 2/3) → **504**.

En consola: error de timeout con `thread_id` y `limit_s=15`.

**Nota:** a los ~15 s la API **decide** el 504. Postman (u otro cliente) puede recibirla **un poco después** si el LLM/SDK sigue en el hilo de fondo. Lo que cuenta: status **504** + log `limit_s=15`, no el cronómetro exacto del cliente.

Luego volvemos a **300** (u otro margen) y reiniciamos.

### 7) Cliente Streamlit (dado)

Con la API en `:8000` y los TODOs hechos:

1. En `../02_cliente_streamlit/`: `cp .env.example .env` (misma `API_KEY` que el servidor).
2. `streamlit run app.py`.
3. **Preguntar (con clave)** → 200; **sin clave** → 401; **Ver historial** → messages.

---

## Checklist

- [ ] `/health` sin clave → 200.
- [ ] `/ask` sin `api_key` → 401; con `?api_key=` → 200 + log `thread_id` / `duration_ms`.
- [ ] GET messages con clave → historial; sin clave → 401.
- [ ] Forzamos **429** (rate limit bajo + GET messages).
- [ ] Forzamos **504** (`ASK_TIMEOUT_SECONDS` bajo) y volvemos a un margen holgado.
- [ ] `python verificar.py --check` OK.
- [ ] (Opcional) Cliente Streamlit: ask / 401 / historial.

---

## Experimentos opcionales

1. **503 (servidor mal configurado):** quitad `API_KEY` del `.env` del servidor, reiniciad uvicorn, llamad `/ask` con cualquier clave → **503**. Luego volved a poner la clave y reiniciad. No confundir con **401** (fallo del cliente).
2. **401 con clave mala:** `?api_key=incorrecta` → **401** (igual que sin clave, pero deja claro que “cualquier string” no vale).
3. **Logs limpios:** tras un `/ask` OK, en consola deben verse `thread_id` y `duration_ms`, **sin** el valor de `API_KEY`, `GEMINI_API_KEY` ni de `?api_key=`.
4. **`/health` no cuenta en el cupo:** con rate limit bajo (p. ej. 5), agotad el cupo con GET messages → **429**; `/health` sigue → **200**.
5. **Historial tras un 504:** un `/ask` OK (queda en SQL); luego forzáis 504; GET messages solo muestra el turno que cerró bien.
6. **Cliente Streamlit:** sin `API_KEY` en el `.env` del cliente → aviso en sidebar; con la misma clave que el servidor → ask / historial.
