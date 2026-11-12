![Cabecera](../../assets/cabecera_mlops.png)

# Introducción — local vs cloud

En la unidad de Docker la API ejecuta en un contenedor **en nuestro PC**. El siguiente paso es que alguien llame a una **URL pública HTTPS** sin tener Docker instalado.

```text
Antes (local)
  Cliente → http://127.0.0.1:8000

Ahora (cloud)
  Cliente → https://mi-servicio.onrender.com
                ↓
           contenedor en el PaaS
                ↓
           (si hay historial) Postgres managed
```

## Qué cambia al subir a cloud

| Tema | Local | Cloud (PaaS) |
|------|-------|--------------|
| Cómo arranca | `docker run` / uvicorn | Build desde repo + start |
| Secrets | `.env` / `--env-file` | Variables en el **panel** |
| Disco | Nuestro SSD | Efímero en el web service; BD managed aparte |
| URL | localhost | HTTPS pública |
| Cold start | Casi no | En planes bajos el servicio puede **dormir** |

La **lógica de negocio** (agente, tools, API key, rate limit, logs) **no se reescribe**: viaja en el mismo código / misma imagen.

## PaaS canónico: Render

Elegimos **Render** porque:

- encaja con **Dockerfile**
- secrets por UI
- **Postgres** managed en el mismo ecosistema
- plan free/bajo útil para demos (con límites: cold start, etc.)

Otras plataformas (Railway, Fly, Cloud Run…) existen; el patrón es el mismo: **build → servicio web → env → BD managed**.

## Qué desplegamos (y qué no)

| Pieza | ¿Deploy? |
|-------|----------|
| FastAPI (+ agente / tools) | **Sí** |
| RAG (índice + retrieval en proceso) | **Dentro** del mismo servicio |
| Streamlit | Suele quedarse en **local** apuntando a la URL cloud |
| Redis / vector DB cloud | **No** en este sprint |