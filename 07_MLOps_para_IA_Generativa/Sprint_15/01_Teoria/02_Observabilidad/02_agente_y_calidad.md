![Cabecera](../../assets/cabecera_mlops.png)

# Agente y calidad

El log HTTP del borde dice “200”. Dentro de un turno de agente (tools + LLM) hace falta un poco más de rastro — y una lista corta de comprobación antes de decir “listo”.

## Rastro del turno (RAG, agents, tools)

| Evento | Ejemplo de log |
|--------|----------------|
| Inicio turno | `ask start thread_id=…` |
| Tool | `tool=rag_guia ok duration_ms=…` o `fail` |
| Fin turno | `ask done pending_hitl=false` |

No hace falta trazar cada token. Con tool + ok/fail ya diagnosticamos gran parte de los “no me respondió bien”.

- HTTP log = capa borde.
- Tool log = capa agente.
- Ambas comparten `thread_id`.

En la práctica del sprint, lo mínimo que siempre veremos es el log del borde (`POST /ask thread_id=… duration_ms=…`). El rastro por tool es el siguiente nivel si lo necesitamos.

## Checklist de calidad

No es un lab de evals ni un dataset. Es una **lista de comprobación rápida**:

- `/health` → 200.
- `/ask` con key válida → `respuesta` no vacía (o `pending_hitl` coherente).
- Sin key → 401 (y sale en el log).
- Rate limit forzado → 429.

Si la respuesta del LLM es “rara”, lo anotamos; no construimos un juez automático en este sprint.

## Resumen

- Borde HTTP + (opcional) tools, siempre con `thread_id`.
- Calidad básica = probar a mano los caminos críticos y mirar respuesta y logs.
- Eval formal queda fuera (o para un proyecto posterior).
