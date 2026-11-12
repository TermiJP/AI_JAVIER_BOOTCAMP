# Cliente Streamlit → API calidad del aire

Cliente **dado** (sin TODOs). Llama a la API en [`../01_api_calidad_aire_segura/`](../01_api_calidad_aire_segura/) o a la SOLUTION.

```bash
python -m venv .venv
source .venv/bin/activate
# .venv\Scripts\Activate.ps1       # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env    # misma API_KEY que el servidor
streamlit run app.py
```

La `API_KEY` sale del `.env` de **este** cliente (no se muestra en pantalla).  
Botones: con clave → 200; sin clave → 401; historial → GET messages.
