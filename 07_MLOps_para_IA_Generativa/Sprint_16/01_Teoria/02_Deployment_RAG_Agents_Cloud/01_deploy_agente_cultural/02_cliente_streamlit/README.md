![Cabecera](../../../../assets/cabecera_mlops.png)

# Cliente Streamlit → API agente (opcional)

**No es el backend.** Solo un cliente HTTP hacia la API en `:8000` (uvicorn o Docker).

La guía de Postgres / Docker / Render está en [`../01_api_agente_segura_docker_postgreSQL/`](../01_api_agente_segura_docker_postgreSQL/).

Atajo si la API ya escucha en `:8000`:

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # misma API_KEY que el servidor
streamlit run app.py
```

La `API_KEY` sale del **`.env` de este cliente**.  
Sidebar: URL (o `API_BASE_URL`) + `thread_id`.

Botones: **Preguntar (con clave)** → 200; **sin clave** → 401; **Ver historial** → GET messages.
