![Cabecera](../../../../assets/cabecera_mlops.png)

# Cliente Streamlit → API segura

**No es el backend.** Solo un cliente HTTP hacia [`../01_api_segura_crud_docker/`](../01_api_segura_crud_docker/) (uvicorn o Docker).

La guía de arranque unificada está en el **[README raíz](../README.md)**.

Atajo si la API ya escucha en `:8000`:

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # misma API_KEY que el servidor / contenedor
streamlit run app.py
```

La `API_KEY` sale del **`.env` de este cliente**.  
Sidebar: URL (o `API_BASE_URL`) + `limit`.

Botones: **Listar con clave** → 200; **sin clave** → 401.
