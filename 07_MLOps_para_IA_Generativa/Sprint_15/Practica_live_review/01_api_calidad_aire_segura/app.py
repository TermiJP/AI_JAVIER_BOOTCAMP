"""
API FastAPI — agente calidad del aire + historial SQLite + capa segura (alumno).

TODO 3: CORSMiddleware leyendo config.CORS_ORIGINS
TODO 4: logs INFO con thread_id + duration_ms en POST /ask
TODO 5: timeout ASK_TIMEOUT_SECONDS → 504 en POST /ask

Público: /health · Protegido: /ask, /approve, GET messages (Depends ya cableado)
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import config
from gemini_auth import configurar_gemini_api_key
from schemas import ApproveIn, AskIn, AskOut, MessageOut
from security import require_api_key
from src import db
from src.agent import aprobar_plan, procesar_turno
from src.state import crear_estado

configurar_gemini_api_key()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

_sessions: Dict[str, dict] = {}
_last_pregunta: Dict[str, str] = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.ensure_schema()
    yield


app = FastAPI(
    title="API agente calidad del aire segura (alumno)",
    description=(
        "Agente LangGraph + historial SQLite. Completad seguridad, CORS, logs y timeout."
    ),
    lifespan=lifespan,
)

# TODO 3: app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, ...)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


def _estado_sesion(thread_id: str, pedido: str = "") -> dict:
    if thread_id not in _sessions:
        _sessions[thread_id] = crear_estado(pedido)
    return _sessions[thread_id]


def _a_ask_out(estado: dict, thread_id: str) -> AskOut:
    return AskOut(
        respuesta=estado.get("respuesta") or "",
        thread_id=thread_id,
        done=bool(estado.get("done", False)),
        pendiente_hitl=bool(estado.get("pendiente_hitl", False)),
        error=estado.get("error") or None,
    )


def _persistir_si_hay_respuesta(thread_id: str, pregunta: str, estado: dict) -> None:
    respuesta = (estado.get("respuesta") or "").strip()
    if not respuesta:
        return
    db.save_turn(thread_id, pregunta, respuesta)


@app.get("/health")
def health():
    return {"status": "ok", "storage": db.storage_mode()}


@app.post("/ask", response_model=AskOut, dependencies=[Depends(require_api_key)])
def ask(body: AskIn) -> AskOut:
    pregunta = body.pregunta.strip()
    if not pregunta:
        raise HTTPException(status_code=400, detail="pregunta vacía")

    thread_id = (body.thread_id or "default").strip() or "default"
    estado = _estado_sesion(thread_id, pedido=pregunta)
    _last_pregunta[thread_id] = pregunta

    t0 = time.perf_counter()

    # TODO 5: envolver el turno con _con_timeout (ThreadPoolExecutor + ASK_TIMEOUT_SECONDS)
    #         y capturar FuturesTimeoutError → HTTPException 504
    out = procesar_turno(estado, pregunta, thread_id)
    if body.auto_aprobar and out.get("pendiente_hitl"):
        out = aprobar_plan(thread_id, True, out)

    _sessions[thread_id] = out

    if not out.get("pendiente_hitl"):
        _persistir_si_hay_respuesta(thread_id, pregunta, out)

    # TODO 4: duration_ms = int((time.perf_counter() - t0) * 1000)
    # TODO 4: logger.info("POST /ask thread_id=%s duration_ms=%s ...", thread_id, duration_ms, ...)

    return _a_ask_out(out, thread_id)


@app.post("/approve", response_model=AskOut, dependencies=[Depends(require_api_key)])
def approve(body: ApproveIn) -> AskOut:
    thread_id = body.thread_id.strip()
    if thread_id not in _sessions:
        raise HTTPException(
            status_code=404,
            detail="No hay sesión para ese thread_id. Haz antes un POST /ask.",
        )

    estado = _sessions[thread_id]
    if not estado.get("pendiente_hitl"):
        raise HTTPException(
            status_code=400,
            detail="No hay plan pendiente de aprobación en este hilo.",
        )

    out = aprobar_plan(thread_id, body.aprobado, estado)
    _sessions[thread_id] = out

    pregunta = _last_pregunta.get(thread_id, "")
    if pregunta and not out.get("pendiente_hitl"):
        _persistir_si_hay_respuesta(thread_id, pregunta, out)

    return _a_ask_out(out, thread_id)


@app.get(
    "/threads/{thread_id}/messages",
    response_model=list[MessageOut],
    dependencies=[Depends(require_api_key)],
)
def get_messages(thread_id: str) -> list[MessageOut]:
    rows = db.list_messages(thread_id)
    return [MessageOut(**row) for row in rows]
