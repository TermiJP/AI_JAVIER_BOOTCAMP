![Cabecera](../../assets/cabecera_mlops.png)

# Render, FastAPI y secrets

## Flujo típico

1. Repo en GitHub con `Dockerfile` (raíz del servicio).
2. En Render: **New → Web Service** → conectar el repo → entorno **Docker**.
3. Definir **Environment Variables** en el panel.
4. Deploy → URL `https://….onrender.com`.
5. Probar `/health` y un `/ask?api_key=…` (Swagger, curl, cliente local).

```text
GitHub push (o Deploy manual)
        ↓
   Render build (Dockerfile)
        ↓
   Contenedor + env del panel
        ↓
   https://servicio.onrender.com
```

## Secrets en el panel

Mismas claves que en local, **sin** subir `.env` al repo:

| Variable | Uso |
|----------|-----|
| `API_KEY` | Auth de nuestra API (`?api_key=`) |
| `GEMINI_API_KEY` | LLM / visión |
| `GEMINI_MODEL` | Modelo (opcional; la app puede tener default) |
| `ASK_TIMEOUT_SECONDS` | Timeout del `/ask` → 504 |
| `CORS_ORIGINS` | Orígenes permitidos (front / Streamlit) |
| `DATABASE_URL` | Postgres managed (si hay historial) |

En el código: `os.getenv`. Si falta un secreto crítico, la app debe **fallar claro** — no hardcodear defaults de producción.

`PORT` lo inyecta el hosting; el Dockerfile ya usa `${PORT:-8000}`.

## Health check

El PaaS puede pegarle a `/health`. Ese endpoint debe ser **ligero** (sin LLM) y sin exigir API key (si no, el health check falla).

Con historial en Postgres, esperad algo como:

```json
{"status": "ok", "storage": "postgres"}
```

## Logs

`print` / logging a **stdout** aparecen en el dashboard (Logs). Request id, latencia y errores sirven igual que en local.

## Streamlit como cliente (opcional)

```text
Streamlit (tu PC)  --HTTPS-->  FastAPI en Render
```

En el cliente: URL base pública + la misma `API_KEY`. No hace falta desplegar Streamlit para validar el backend.

## Fallos frecuentes

| Síntoma | Pista |
|---------|--------|
| Build OK, servicio cae | Falta env (`API_KEY`, `GEMINI_API_KEY`, `DATABASE_URL`) o crash al importar |
| 401 en todo | `API_KEY` del panel ≠ `?api_key=` del cliente |
| Timeout / 504 | `ASK_TIMEOUT_SECONDS`, cold start, o LLM lento |
| CORS en el browser | Origen del front no está en `CORS_ORIGINS` |

---

Siguiente: [RAG en el contenedor](./02_rag_en_el_contenedor.md).
