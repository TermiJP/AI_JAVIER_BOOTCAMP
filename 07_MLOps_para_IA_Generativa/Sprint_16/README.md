![Cabecera](assets/cabecera_mlops.png)

# 📘 Sprint 16 — Deployment & Cloud Systems

En el Sprint 15 la API quedó **segura y observable en local**. Aquí el salto: **empaquetar**, **publicar** y **automatizar**.

> **¿Cómo empaquetamos, desplegamos y automatizamos** lo que ya construimos?

**Cómo se consume este sprint:** soltamos los **3 bloques de golpe**. Leéis teoría + ejemplos, seguís los **workouts** (repos + vídeos de las demos) y os autoconsumís el material. **No hay entregables** de workout. El **único ejercicio** es la **Live Review** (deploy de la API calidad del aire); antes hay un **taller de ~2 días** para ver cómo montarla.

---

## Mapa del módulo (Sprints 14–16)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| 14 | ¿Cómo expongo el sistema como API y persisto datos? | Backend |
| 15 | ¿Cómo dejo el sistema seguro, robusto y visible en local? | Production-ready |
| **16** (este) | ¿Cómo empaqueto, publico y automatizo? | Deploy + CI/CD |

```text
S15     Seguridad + observabilidad (local)
 ↓
S16     Docker → Render/agente → costes + CI/CD → LR aire en cloud
 ↓
        Project Break 3  →  Project_Break/PB_03_MLOps
```

Enunciado del cierre: [Project Break 3 — MLOps](../../Project_Break/PB_03_MLOps/).

**Prerrequisito:** Sprint 15.  
**PaaS canónico:** Render. **BD managed:** Postgres cuando haya historial.  
**RAG:** viaja **dentro** del mismo contenedor FastAPI (no es un servicio aparte).  
**No entra:** Kubernetes · OAuth completo · Redis hands-on · vector DB cloud · Compose como camino a PaaS · obs enterprise.

---

## 🧭 Docker y containerización

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/01_Docker_y_containerizacion/00_introduccion.md) | Por qué Docker |
| [Containers e imágenes](./01_Teoria/01_Docker_y_containerizacion/01_containers_e_imagenes.md) | VS VM · build/run |
| [Dockerfile y FastAPI](./01_Teoria/01_Docker_y_containerizacion/02_dockerfile_y_fastapi.md) | Empaquetar la API |
| [Env, prácticas y Postgres al lado](./01_Teoria/01_Docker_y_containerizacion/03_env_practicas_y_compose.md) | Secrets · runtime · Postgres con `docker run` |

| Workout | Descripción |
|---------|-------------|
| [01_Docker-API-Segura-CRUD](./02_Workout/01_Docker_y_containerizacion/) | API segura (CRUD) + Docker (+ Render opcional). Demo + vídeo; **no entregable**. |

---

## ☁️ Deployment de RAG y Agents en cloud

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/02_Deployment_RAG_Agents_Cloud/00_introduccion.md) | Local vs cloud |
| [Render, FastAPI y secrets](./01_Teoria/02_Deployment_RAG_Agents_Cloud/01_render_fastapi_y_secrets.md) | Web Service · env en panel |
| [RAG en el contenedor](./01_Teoria/02_Deployment_RAG_Agents_Cloud/02_rag_en_el_contenedor.md) | No hace falta “RAG Service” |
| [PostgreSQL local y cloud](./01_Teoria/02_Deployment_RAG_Agents_Cloud/03_postgres_managed.md) | Docker + pgAdmin · managed · `DATABASE_URL` |

| Workout | Descripción |
|---------|-------------|
| [01_deploy_agente_cultural](./02_Workout/02_Deploy_agente_cultural_docker_postgreSQL/) | Agente cultural + Docker + Postgres (+ Render). Demo + vídeo; **no entregable**. |

---

## 🔧 Arquitectura, costes + CI/CD

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/03_Arquitectura_costes_y_CICD/00_introduccion.md) | Mapa 3a + 3b |
| [Arquitectura y costes](./01_Teoria/03_Arquitectura_costes_y_CICD/01_arquitectura_y_costes.md) | Límites · cold start · coste infra/tokens |
| [CI/CD con GitHub Actions](./01_Teoria/03_Arquitectura_costes_y_CICD/02_cicd_github_actions.md) | Idea de pipeline (test → build); sin workout aparte |

---

## 🎯 Practica live review

**Único ejercicio del sprint:** API **calidad del aire** (segura, ya dada) + PostgreSQL + Docker + Render.

→ [`Practica_live_review/`](./Practica_live_review/)

Taller presencial/online (~2 días) para repasar el montaje antes de que lo hagáis vosotros.

---

## Escalera pedagógica

```text
Teoría Docker + workout (vídeo) → Teoría deploy + workout (vídeo) → Teoría costes y CI/CD (vídeo)
     ↓
Taller LR (2 días) → Live Review aire deploy → Project Break 3
```

---

## Infra en cloud (resumen)

| Pieza | ¿Deploy? |
|-------|----------|
| FastAPI (+ RAG/agent en el mismo contenedor) | **Sí** — Render |
| Postgres managed | **Sí** — cuando haya historial SQL |
| Redis / vector DB | No (solo mención) |
| Streamlit | Local apuntando a la URL cloud |
