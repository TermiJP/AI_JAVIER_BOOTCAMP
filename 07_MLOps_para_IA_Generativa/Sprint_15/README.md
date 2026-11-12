![Cabecera](assets/cabecera_mlops.png)

# 📘 Sprint 15 — Production AI Systems

En el Sprint 14 la API (y el agente) funcionan en **local**, pero aún no están listos para exponerse: sin protección de endpoints, sin límites claros y con poca visibilidad de lo que ocurre en cada turno.

Aquí **bajáis a tierra** el sistema: seguridad/robustez + observabilidad, **antes** de desplegar (eso va en S16).

> **¿Cómo dejo el backend de IA seguro, robusto y visible en local?**

> **Nota pedagógica:** en el syllabus institucional este contenido aparece a menudo como “Production” en S16. Aquí lo impartimos en **S15** para no publicar un `/ask` abierto; el deploy queda en S16.

---

## Mapa del módulo (Sprints 14–16)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| 14 | ¿Cómo expongo el sistema como API y persisto datos? | Backend |
| **15** (este) | ¿Cómo dejo el sistema seguro, robusto y visible en local? | Production-ready |
| 16 | ¿Cómo empaqueto, publico y automatizo? | Deploy + CI/CD |

```text
S14     FastAPI (+ agente + SQLModel / SQLite)
 ↓
S15     W1: API key + rate limit + CORS + Streamlit · W2: agente + logs/thread_id + timeout + Streamlit
 ↓
S16     Docker + Render + Postgres managed + CI/CD → Project Break 3
```

**Prerrequisito:** Sprint 14 (CRUD FastAPI + API sobre agente cultural).  
**No entra en este sprint:** Docker en PaaS, Render, CI/CD, Postgres managed.

---

## Stack y dominio

- **Stack:** Python · FastAPI · Pydantic · secrets por env · (W2: agente cultural)
- **W1:** CRUD S14 endurecido
- **W2:** agente cultural + auth + logs/`thread_id` + timeout + cliente Streamlit
- **Live Review:** [calidad del aire segura](./Practica_live_review/) — TODOs API key / logs / timeout

---

## 🧭 Bloque 1 — Seguridad y robustez

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/01_Seguridad_y_robustez/00_introduccion.md) | Por qué proteger antes de desplegar |
| [Autenticación y secrets](./01_Teoria/01_Seguridad_y_robustez/01_autenticacion_y_secrets.md) | Claves, API key / JWT / OAuth, `Depends` |
| [Rate, timeouts y errores](./01_Teoria/01_Seguridad_y_robustez/02_rate_timeouts_y_errores.md) | 429, 504, códigos claros |
| [Seguridad de tools del agente](./01_Teoria/01_Seguridad_y_robustez/03_seguridad_de_tools_del_agente.md) | Qué puede hacer el grafo por dentro |

| Workout | Descripción |
|---------|-------------|
| [01_FastAPI-API-Segura-CRUD](./02_Workout/01_Seguridad_y_robustez/01_FastAPI-API-Segura-CRUD.md) | [Repo](https://github.com/aie-online-tb/Sprint15_FastAPI-API-Segura-CRUD) — API segura (CRUD + API key) + cliente Streamlit |

---

## 🔌 Bloque 2 — Observabilidad

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/02_Observabilidad/00_introduccion.md) | Mapa del bloque |
| [Logs en local](./01_Teoria/02_Observabilidad/01_logs_en_local.md) | Logging, `thread_id`, `duration_ms` |
| [Agente y calidad](./01_Teoria/02_Observabilidad/02_agente_y_calidad.md) | Rastro del turno + checklist |
| [De local a cloud](./01_Teoria/02_Observabilidad/03_de_local_a_cloud.md) | Misma instrumentación hacia S16 |

| Workout | Descripción |
|---------|-------------|
| [01_FastAPI-API-Agente-Cultural-Seguro](./02_Workout/02_Observabilidad/01_FastAPI-API-Agente-Cultural-Seguro.md) | [Repo](https://github.com/aie-online-tb/Sprint15_FastAPI-API-Agente-Cultural-Seguro) — agente cultural + seguridad/obs + cliente Streamlit |

---

## 🎯 Practica live review

Live Review **calidad del aire segura**: mismos agente + historial; TODOs de API key, rate limit, CORS, logs y timeout — **sin** Render.

→ [`Practica_live_review/`](./Practica_live_review/)

---

## Escalera pedagógica

```text
Teoría B1 → W1 CRUD endurecido
     ↓
Teoría B2 → W2 cultural + Streamlit (temario completo)
     ↓
LR calidad del aire (TODOs)
     ↓
Sprint 16 (Docker + PaaS + CI/CD)
```

---

## Fuera de alcance

Docker · Render / PaaS · CI/CD · Postgres managed · JWT hands-on / OAuth · Kubernetes · observabilidad enterprise.
