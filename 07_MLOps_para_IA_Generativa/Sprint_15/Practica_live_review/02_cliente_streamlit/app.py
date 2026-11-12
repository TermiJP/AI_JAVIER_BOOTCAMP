"""
Cliente Streamlit → API agente calidad del aire segura.

POST /ask y GET messages con ?api_key= (desde .env de este cliente).
"""

import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = (os.getenv("API_KEY") or "").strip()
default_base = (os.getenv("API_BASE_URL") or "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="Cliente → Calidad del aire", layout="centered")
st.title("Cliente Streamlit → calidad del aire")
st.caption(
    "Demo HTTP al agente. La API_KEY vive en el `.env` de este cliente (solo local)."
)

with st.sidebar:
    st.header("Conexión")
    if api_key:
        st.success("API_KEY cargada desde `.env`")
    else:
        st.warning("Falta API_KEY en `.env` (copiad `.env.example`).")
    base_url = st.text_input(
        "URL base de la API",
        value=default_base,
        help="uvicorn en 01_api_calidad_aire_segura (puerto 8000).",
    ).rstrip("/")
    thread_id = st.text_input(
        "thread_id",
        value="demo-aire",
        help="Mismo hilo = mismo historial en SQLite.",
    )
    timeout_s = st.number_input(
        "Timeout cliente (s)",
        min_value=30,
        max_value=600,
        value=300,
        help="≥ ASK_TIMEOUT_SECONDS del servidor.",
    )

pregunta = st.text_area(
    "Pregunta al agente",
    value=(
        "Zona centro, contaminante NO2. Consulta la guía y datos de la API "
        "de Madrid. Propón un plan breve."
    ),
    height=100,
)

col1, col2, col3 = st.columns(3)


def _params(*, with_key: bool) -> dict:
    params: dict = {}
    if with_key and api_key:
        params["api_key"] = api_key
    return params


def _mostrar_http(r: requests.Response) -> None:
    st.metric("Status HTTP", r.status_code)
    try:
        body = r.json()
    except ValueError:
        st.text(r.text)
        return

    if r.status_code == 200:
        st.success("200 — OK")
        st.json(body)
    elif r.status_code == 401:
        st.warning("401 — falta api_key o no coincide con el servidor")
        st.json(body)
    elif r.status_code == 429:
        st.warning("429 — rate limit")
        st.json(body)
    elif r.status_code == 504:
        st.error("504 — timeout del servidor (ASK_TIMEOUT_SECONDS)")
        st.json(body)
    else:
        st.error(f"Respuesta {r.status_code}")
        st.json(body)


def _ask(*, with_key: bool) -> None:
    url = f"{base_url}/ask"
    params = _params(with_key=with_key)
    payload = {
        "pregunta": pregunta.strip(),
        "thread_id": (thread_id or "default").strip() or "default",
        "auto_aprobar": True,
    }

    auth_nota = "con api_key" if with_key else "sin api_key (esperamos 401)"
    st.code(
        f"POST /ask  ({auth_nota})\n"
        f"pregunta: {payload['pregunta'][:80]}…\n"
        f"thread_id: {payload['thread_id']}",
        language="text",
    )

    if not pregunta.strip():
        st.warning("Escribí una pregunta.")
        return

    try:
        with st.spinner("Esperando al agente…"):
            r = requests.post(
                url,
                params=params,
                json=payload,
                timeout=float(timeout_s),
            )
    except requests.Timeout:
        st.error(f"El cliente cortó a los {timeout_s}s.")
        return
    except requests.RequestException as exc:
        st.error(f"No pudimos conectar: {exc}")
        st.info("¿uvicorn en 01_api_calidad_aire_segura? :8000")
        return

    _mostrar_http(r)
    if r.status_code == 200:
        data = r.json()
        st.markdown("**Respuesta**")
        st.write(data.get("respuesta", ""))


def _messages(*, with_key: bool) -> None:
    tid = (thread_id or "default").strip() or "default"
    url = f"{base_url}/threads/{tid}/messages"
    params = _params(with_key=with_key)

    st.code(f"GET /threads/{tid}/messages", language="text")

    try:
        r = requests.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        st.error(f"No pudimos conectar: {exc}")
        return

    _mostrar_http(r)
    if r.status_code == 200:
        rows = r.json()
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("Historial vacío.")


with col1:
    if st.button("Preguntar (con clave)", type="primary", use_container_width=True):
        if not api_key:
            st.warning("Falta API_KEY en el `.env` del cliente.")
        else:
            _ask(with_key=True)

with col2:
    if st.button("Preguntar sin clave → 401", use_container_width=True):
        _ask(with_key=False)

with col3:
    if st.button("Ver historial", use_container_width=True):
        if not api_key:
            st.warning("Falta API_KEY en el `.env` del cliente.")
        else:
            _messages(with_key=True)
