![Cabecera](../../07_MLOps_para_IA_Generativa/Sprint_16/assets/cabecera_mlops.png)

# Project Break 3 — MLOps: API, datos y deploy

**Duración:** 2 semanas

**Entrega:** como tarde el **26/11 hasta las 23:59**.

**Presentación:** viernes **4 de diciembre, de 16:00 a 18:00**.

Publicar en equipo el **agente del Project Break 2**: una API REST con FastAPI (y su Swagger), el agente detrás de esa API, historial en **PostgreSQL**, imagen **Docker**, despliegue en **Render** y un **front** que consume la URL pública.

Esta práctica integra MLOps para IA generativa:

- **FastAPI, contrato Pydantic, agente detrás de `/ask` y historial SQL** (Sprint 14)
- **API key, rate limit, timeout, CORS y logs** (Sprint 15)
- **Docker, Render, Postgres managed y lectura de costes** (Sprint 16). El CI/CD de ese sprint aquí no es obligatorio.

---

## Contexto: pieza de un puzzle

Este Project Break es la **tercera pieza** de un proyecto incremental del bootcamp:

| Pieza | Proyecto | Rol |
|-------|----------|-----|
| **1** | [Project Break RAG](../PB_01_RAG/) | Sistema RAG modular y usable |
| **2** | [Project Break Agentes · LangGraph](../PB_02_Agentes_LangGraph/) | Ese RAG como **tool** de un agente multiagente |
| **3** | **Project Break MLOps** | Ese agente, publicado: API + PostgreSQL + Docker + Render |

Partís del **mismo equipo, el mismo dominio y el código del PB2**. El RAG sigue siendo una tool. El trabajo de estas dos semanas es **sacarlo de la máquina local** y dejarlo como servicio.

Misma arquitectura que los workouts y la live review de los Sprints 14–16 (API cultural / calidad del aire). Aquí el dominio es el vuestro.

```text
Front Streamlit (en local)
        │  HTTPS   API_BASE_URL = URL de Render
        ▼
FastAPI  +  agente PB2  +  RAG          ← un solo contenedor en Render
        │  /health   /docs   /ask   /approve   /threads/{id}/messages
        │  DATABASE_URL
        ▼
PostgreSQL managed (Render)
```

---

# Objetivos generales

Dejar el agente del PB2 como un servicio que:

1. Expone una **API REST** con FastAPI y la documentación viva en **Swagger** (`/docs`).
2. Mete el agente **dentro** de la API (`POST /ask`, `POST /approve`), sin reescribir el grafo.
3. Guarda el historial de turnos cerrados en **PostgreSQL** (SQLModel).
4. Viaja en **una imagen Docker** (API + agente + RAG en el mismo contenedor).
5. Está **desplegado en Render** (Web Service + Postgres), con secretos en el panel.
6. Se **usa desde un front** apuntando a esa URL pública.

---

## Entregables finales

> **Fecha límite de entrega: 26/11, hasta las 23:59.** Con la URL del despliegue, el repositorio y el informe ya entregados a esa hora.

1. **Repositorio GitHub** desde el primer día, con código reproducible, `.env.example`, `.gitignore`, `Dockerfile` y README del equipo.
2. **API en local y en Render**, con Swagger abierto en la URL pública.
3. **PostgreSQL** con historial que **sigue ahí después de un redeploy**.
4. **Front Streamlit** configurado contra la URL de Render (chat, historial leído de la API, HITL).
5. **URL del despliegue**, enviada al profesorado. Con esa URL tenemos que poder entrar al producto: `/docs` y `/health` abren. Para probar `/ask` y el historial, adjuntad la API key de demo por el canal de entrega (no la subáis al repositorio).
6. **Informe breve** (`entregables/informe_decisiones.md`), con las conclusiones de arquitectura, coste y CI/CD.
7. **Presentación final** (~10 min) en vivo o vídeo; **sólo se permite un vídeo por grupo**. La demo de producto se hace contra la **URL desplegada**.

---

## Trabajo en equipo y Git

Gestión del proyecto con **GitHub desde el primer día**. La organización interna la decidís vosotros.

Podéis crear un **repo nuevo** y copiar el código del PB2, o seguir en el mismo repo si `main` del PB2 queda etiquetado y este trabajo vive en ramas claras. El README de entrega tiene que arrancar **este** servicio, no solo el CLI del PB2.

### Reglas mínimas

- Crear el **repositorio en GitHub** al inicio del proyecto.
- **Mínimo una PR revisada y mergeada por miembro** del equipo.
- Integrar con **pull requests** hacia `develop`; resolver conflictos en la rama antes del merge.
- **No subir claves** — usar `.env` y `.gitignore`. En Render, las claves van en el panel del servicio.
- README del repo: clonar, Postgres en local, variables, `docker build` / `docker run`, URL de Render, cómo abrir Swagger y cómo arrancar el front contra esa URL.

### Buenas prácticas con Git

| Rama | Uso |
|------|-----|
| `main` | Código estable y el que Render despliega. **No trabajéis directamente aquí.** |
| `develop` | Integración del equipo. |
| Ramas secundarias | Una por bloque de trabajo, desde `develop`. |

**Convención de ramas** (ejemplos):

- `feature/api-ask`
- `feature/postgres-historial`
- `feature/dockerfile`
- `feature/front-url-render`
- `fix/port-render`
- `update/requirements`

```text
develop ──► feature/tu-tarea ──► commits ──► PR ──► merge a develop
       └──► cuando todo esté listo ──► merge a main ──► Render redespliega
```

- Commits **pequeños y con mensaje claro**.
- **Nunca** subáis `.env`, `.venv/`, dumps de Postgres ni secretos.
- Antes de mergear a `main`, `develop` debe poder levantar la API en local (Docker) y pasar el CI.

---

## Forma de trabajo · Spec-Driven Development (SDD)

**SDD forma parte de cómo afrontar este Project Break.** Acordad por escrito el contrato HTTP (rutas, bodies, códigos) **antes** de pedir código al asistente. Así no os reescribe el grafo ni mete la lógica del agente dentro del front.

No es un ítem del checklist de entrega ni un porcentaje de la rúbrica base. Si dejáis evidencia clara en el repo o en el informe, puede sumar en **Extras**.

---

## Estructura de proyecto

Ejemplo **orientativo**. Los nombres pueden variar; la separación, no.

```text
project_break_mlops/
├── README.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── config.py                 # DATABASE_URL, API_KEY, timeout, CORS, límites
├── app.py                    # FastAPI: rutas
├── schemas.py                # AskIn, AskOut, ApproveIn, MessageOut
├── security.py               # API key, rate limit (o módulos equivalentes)
├── src/
│   ├── db.py                 # engine, create_all, sesión
│   ├── models.py             # SQLModel: Conversation y Message recomendadas; las tablas que necesitéis
│   ├── agent.py              # procesar_turno / aprobar_plan  (PB2)
│   ├── graph.py              # grafo del PB2
│   └── tools/                # allowlist del PB2
├── rag/                      # RAG del PB1/PB2, dentro de la imagen
├── data/
├── front/
│   └── streamlit_app.py      # cliente HTTP. No importa el grafo.
└── entregables/
    └── informe_decisiones.md
```

En este proyecto **`app.py` es la API**. El front vive aparte y solo habla HTTP.

---

## De qué partís (PB2)

Reutilizad el agente que ya funciona:

- Grafo multiagente, tools (RAG completo, API externa, auxiliar, multimodal) y allowlist.
- `procesar_turno` y la decisión humana (`aprobar` / `rechazar`).
- Límites en Python (`max_turns`, `max_steps`, `done`).
- Checkpointer **`MemorySaver`** en el proceso. El historial de producto pasa a Postgres; el checkpoint del grafo **sigue en memoria**.

Un reinicio del servicio pierde un HITL a medias. El historial SQL no. Explicadlo en el informe en un párrafo. Llevar el checkpoint de LangGraph a Postgres queda fuera.

El dominio sigue siendo el del PB1/PB2. Los dominios de clase (agenda cultural, calidad del aire) no sustituyen al vuestro.

---

## Capacidades del sistema

### 1. API REST y Swagger

FastAPI con contrato Pydantic. Swagger (`GET /docs`) se genera solo y tiene que abrir **sin API key**, en local y en la URL de Render.

| Método | Ruta | ¿`api_key`? | Qué hace |
|--------|------|-------------|----------|
| GET | `/health` | No | Pulso. Incluye que el almacenamiento es Postgres |
| GET | `/docs` | No | Swagger con los schemas |
| POST | `/ask` | **Sí** | Un turno del agente |
| POST | `/approve` | **Sí** | HITL: aprobar o rechazar el plan |
| GET | `/threads/{thread_id}/messages` | **Sí** | Historial leído de Postgres |

Contrato alineado con el Sprint 14 (los nombres exactos pueden ser los vuestros si el comportamiento es este):

- **AskIn:** `pregunta`, `thread_id`, `auto_aprobar` (por defecto `true`, cómodo para probar en Swagger).
- **AskOut:** `respuesta`, `thread_id`, `done`, `pendiente_hitl`, `error`.
- **ApproveIn:** `thread_id`, `aprobado` (`true` aprueba, `false` rechaza).
- **MessageOut:** `role`, `content`, y el orden temporal.

`/health` y `/docs` públicos. El resto exige `api_key` (query, como en los workouts, para poder probarlo en Swagger). Sin clave → **401**. Body inválido → **422**.

### 2. El agente, dentro de la API

`POST /ask` llama a `procesar_turno` (o equivalente). `POST /approve` llama a la decisión humana del PB2.

- Con `auto_aprobar=true`, si el grafo queda en HITL la API cierra el turno sola (útil en Swagger).
- Con `auto_aprobar=false`, la respuesta vuelve con `pendiente_hitl=true` y el front usa `POST /approve`.
- Las tools siguen siendo reales: una pregunta de dominio tiene que poder apoyarse en el RAG o en la API externa.
- Los límites y `done` los sigue decidiendo Python.

### 3. PostgreSQL

El historial vive en PostgreSQL, con SQLModel. El modelo de datos lo diseñáis vosotros, según lo que el producto necesite guardar.

Como punto de partida recomendado, dos tablas cubren el turno: **`Conversation`** y **`Message`**, unidas por `thread_id`. Podéis añadir las tablas que os hagan falta (por ejemplo usuario, feedback o traza de tools). `create_all` al arrancar es suficiente.

```text
POST /ask
  1. asegura la conversación de ese thread_id
  2. ejecuta el turno
  3. si el turno queda cerrado (done): guarda user + assistant y hace commit
GET /threads/{thread_id}/messages
  → los mensajes de ese hilo, en orden
```

`DATABASE_URL` sale del entorno.

- **Local:** Postgres de verdad (un contenedor Docker, o la URL externa de Render mientras desarrolláis).
- **Render:** Postgres managed. La URL va en el panel, no en el repo.
- Render a veces entrega `postgres://…`. SQLAlchemy quiere `postgresql://…`: normalizad el prefijo en `config.py` y añadid el driver (`psycopg2-binary` o `psycopg`).

La demo y el servicio público usan Postgres.

**Prueba que pedimos:** un turno cerrado en la URL pública, redeploy (o reinicio), y `GET …/messages` sigue devolviendo ese turno.

### 4. Seguridad y logs (para poder publicarlo)

Lo visto en el Sprint 15, con los mismos códigos:

| Situación | Código |
|-----------|--------|
| Sin `api_key` o clave incorrecta en ruta protegida | **401** |
| Servicio sin `API_KEY` configurada | **503** |
| Por encima de `RATE_LIMIT_PER_MINUTE` | **429** |
| El turno supera `ASK_TIMEOUT_SECONDS` | **504** |

- CORS abierto a lo que necesite el front (`CORS_ORIGINS`).
- Un log por petición protegida: método, ruta, `thread_id`, `duration_ms`, status. Sin `API_KEY`, sin la clave del LLM y sin la connection string.
- El **429** se demuestra en local contra una ruta que no gasta LLM (`GET …/messages` vale). En Render la variable queda puesta y documentada.
- El **504** se demuestra en local bajando el timeout; en Render dejáis un valor con margen para un turno real del multiagente (en clase, el ejemplo holgado es 300 s).

### 5. Docker

Una imagen. Dentro van la API, el agente, el corpus y el índice del RAG (construido en el `docker build` o al arrancar; documentad cuál).

- `Dockerfile` + `.dockerignore` (sin `.env`, sin `.venv`, sin `.git`).
- El proceso escucha en `0.0.0.0` y en el puerto `${PORT:-8000}`. Render inyecta `PORT`.
- `docker build` y `docker run` en local, con `DATABASE_URL` apuntando al Postgres, tienen que responder en `/health`.

### 6. Render

Un **Web Service** (la imagen) y un **PostgreSQL** en la misma cuenta.

Variables en el panel, como mínimo:

- `DATABASE_URL`
- `API_KEY`
- clave del LLM (`GEMINI_API_KEY` o la del proveedor que ya uséis)
- `CORS_ORIGINS`
- `ASK_TIMEOUT_SECONDS`
- `RATE_LIMIT_PER_MINUTE`

El push a `main` redespliega (auto-deploy de Render). Con eso basta: no pedimos un pipeline de CI/CD.

### 7. Front de la API desplegada

Streamlit en **local**. En la demo final, `API_BASE_URL` es la URL de Render, no `localhost`.

El front tiene que poder mostrar:

- el estado que devuelve `GET /health` (servicio vivo y Postgres);
- un chat que hace `POST /ask`;
- el historial del `thread_id`, leído con `GET …/messages` (sale de Postgres, no de una lista solo en memoria del front);
- **Aprobar** y **Rechazar**, llamando a `POST /approve` con `auto_aprobar=false` en el turno;
- el `thread_id` visible. «Nueva conversación» = otro `thread_id`.

La `API_KEY` va en el `.env` del front, igual que en clase. El front no importa `graph.py` ni ejecuta tools.

---

## Requisitos obligatorios

1. FastAPI con las rutas de la tabla y Swagger en `/docs` (local y Render).
2. El agente del PB2 responde por `/ask` y se cierra por `/approve` (o `auto_aprobar`).
3. PostgreSQL en local y en Render. Historial que sobrevive a un redeploy.
4. API key, 401 / 429 / 504, CORS y log con `thread_id` + `duration_ms`.
5. Un `Dockerfile` que respeta `PORT` y lleva el RAG dentro.
6. URL pública de Render, **enviada al profesorado** para que podamos entrar (`/docs`, `/health`, y la API key de demo por el canal de entrega). Secretos fuera del repo.
7. Front Streamlit contra esa URL: health, chat, historial, HITL.
8. README + `.env.example` + `requirements.txt`.
9. Informe en `entregables/` y presentación ~10 min (**sólo se permite un vídeo por grupo**).

---

## Fuera de alcance

Kubernetes · JWT / OAuth · Redis · Alembic · varias réplicas · desplegar el propio Streamlit · base vectorial en la nube · un servicio RAG aparte · checkpoint de LangGraph en Postgres · cambiar de dominio · rehacer el multiagente desde cero.

**CI/CD no es obligatorio.** GitHub Actions (tests, `docker build` en cada push) no forma parte de la entrega. Si lo montáis, puede sumar como extra.

---

# Partes del proyecto

## Parte 1 — Contrato y agente dentro de la API

**Objetivo:** el PB2 responde por HTTP en local, y Swagger lo enseña.

1. Fijar rutas, bodies y códigos (la tabla de arriba) en el README.
2. Pydantic: `AskIn`, `AskOut`, `ApproveIn`, `MessageOut`.
3. `POST /ask` y `POST /approve` llaman al agente que ya tenéis.
4. Probar en `http://127.0.0.1:8000/docs` un turno con `auto_aprobar=true`.

**Criterios de aceptación:**

- [ ] `/docs` lista las rutas y los schemas
- [ ] Un `/ask` con clave devuelve `AskOut` y se nota una tool real (RAG o API)
- [ ] `auto_aprobar=false` deja `pendiente_hitl=true`; `/approve` cierra o rechaza

---

## Parte 2 — PostgreSQL

**Objetivo:** el turno cerrado queda en una base de verdad, no en un fichero que Render va a borrar.

1. Modelo de datos propio. Recomendamos `Conversation` y `Message` como base, y las tablas extra que el producto necesite. `DATABASE_URL`. Normalizar `postgres://`.
2. Guardar user + assistant cuando el turno cierra.
3. `GET /threads/{thread_id}/messages`.
4. Postgres en local. `/health` indica almacenamiento Postgres.

**Criterios de aceptación:**

- [ ] Tras reiniciar el proceso, el GET sigue devolviendo el turno
- [ ] Dos `thread_id` distintos no mezclan mensajes

---

## Parte 3 — Seguridad, logs y front

**Objetivo:** la API se puede enseñar, y el front ya habla con ella.

1. `api_key`, rate limit, timeout, CORS.
2. Log de `thread_id` y `duration_ms`.
3. Front: health, chat, historial desde la API, Aprobar / Rechazar.

**Criterios de aceptación:**

- [ ] 401, 429 y 504 se ven en local (el 429 y el 504, como dice la sección 4)
- [ ] El front, apuntando a la API local, aprueba o rechaza un plan

---

## Parte 4 — Docker, Render, informe y cierre

**Objetivo:** la misma API, en una URL pública, y el front apuntando ahí.

1. `Dockerfile`. `docker run` en local contra Postgres.
2. Web Service + Postgres en Render. Variables en el panel.
3. Comprobar en la URL pública: `/docs`, `/health`, `/ask` con tool, `GET messages`.
4. Redeploy. El mensaje sigue.
5. Front con `API_BASE_URL` = URL de Render. Repetir un turno y un HITL.
6. Enviar al profesorado la URL del servicio (y la API key de demo por el canal de entrega) para que podamos entrar.
7. Informe en `entregables/informe_decisiones.md` con al menos:

   1. **Dibujo** del sistema desplegado (front, API, Postgres, LLM)
   2. **Contrato:** qué es público y qué lleva `api_key`
   3. **Datos:** qué hay en Postgres y qué se pierde si el proceso reinicia (`MemorySaver`)
   4. **Prueba de vida:** turno, redeploy, el GET sigue. Pegad la URL que enviáis al profesorado
   5. **Conclusiones de arquitectura y coste**, sobre vuestro servicio en Render (una página como mucho):
      - qué piezas hay (front local, un Web Service con API + agente + RAG, Postgres) y por qué la API va en un solo contenedor
      - un límite que hayáis notado de verdad (cold start, RAM, timeout o cuota del LLM) y qué efecto tuvo en la demo
      - escalado: el primer paso si hubiera más usuarios (subir plan) y qué no montáis (varias réplicas, colas)
      - dos facturas, con un orden de magnitud: infra (web + Postgres) y tokens de un `/ask`
   6. **Conclusiones de CI/CD.** No hace falta tener GitHub Actions. Sobre vuestro repo y vuestra URL:
      - qué comprobaríais antes de cada deploy: un test que no llama al LLM y un `docker build`
      - dónde están los secretos (panel de Render y `.env` local) y por qué no van al repositorio ni a los logs
      - cómo desplegáis ahora (push a `main` y Render redespliega) y qué es un rollback en vuestro caso (volver al deploy anterior)
      - qué separa desarrollo de producción: la máquina local frente a las variables del servicio
   7. **3 fallos** y qué haríais después

**Criterios de aceptación:**

- [ ] `https://<vuestro-servicio>.onrender.com/docs` abre
- [ ] `/health` en esa URL habla de Postgres
- [ ] Un turno sobrevive a un redeploy
- [ ] El front de la demo usa esa URL
- [ ] La URL (y la API key de demo, fuera del repo) está enviada al profesorado
- [ ] No hay secretos en el repo

---

## Experimentos opcionales

No sustituyen los requisitos. Si os sobra tiempo, documentad 1–3 en el informe:

- [ ] **CI con GitHub Actions** (no obligatorio): un job que corra checks sin llamar al LLM, y otro con `docker build`
- [ ] **Pregunta in-corpus y abstención** disparadas desde Swagger en la URL pública
- [ ] **Multimodal** desde el front, con la imagen que ya va en la imagen Docker
- [ ] **Uso sostenido de SDD** (el contrato HTTP escrito antes del código, visible en el repo)

---

## Stack de referencia

Python · FastAPI · Pydantic · SQLModel · PostgreSQL · Docker · Render · Streamlit como cliente HTTP · el LLM y el RAG que ya usabais en el PB2 (Gemini, si seguís el módulo).

---

## Requisitos técnicos

- Python 3.10+
- Claves solo en `.env` local y en el panel de Render

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # DATABASE_URL, API_KEY, clave del LLM
```

La imagen tiene que arrancar así, en espíritu:

```dockerfile
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```

---

## Orden sugerido y plan de 2 semanas

| Semana | Orientación |
|--------|-------------|
| **1** | Partes 1–3: contrato, agente en la API, Postgres, seguridad, front contra local |
| **2** | Parte 4: Docker, Render, front contra la URL pública, informe, presentación |

Dejad el deploy para cuando `/ask` y el historial ya funcionen en local. Render no depura un grafo roto.

---

## Presentación final (~10 min)

**Fecha:** viernes 4 de diciembre, de 16:00 a 18:00.

**Obligatoria.** En vivo o en **vídeo**. **Sólo se permite un vídeo por grupo.**

Si presentáis en vivo, el vídeo de respaldo cubre un fallo de red o de cold start. Arrancad la URL un minuto antes: el free tier puede estar dormido.

### Guion de tiempo (orientativo)

| Bloque | Tiempo | Enfoque |
|--------|--------|---------|
| A · Producto | ~4 min | El mismo agente de siempre, ahora en una URL. Demo en el front |
| B · Técnico | ~6 min | Contrato, Postgres, Docker, Render |

### A · Producto (~4 min)

- [ ] El problema, en una frase, y la URL pública.
- [ ] Front contra Render: una pregunta de dominio.
- [ ] Historial que sale de `GET …/messages`.
- [ ] HITL: aprobar **o** rechazar, y el efecto en pantalla.

### B · Técnico (~6 min)

- [ ] Swagger de la URL pública (`/docs`).
- [ ] `/health` y un 401 (sin clave).
- [ ] Dónde está el agente (la ruta llama a `procesar_turno`; el front no lo importa).
- [ ] Postgres: tablas, y el turno que sigue tras el redeploy.
- [ ] `Dockerfile` (`PORT`, RAG dentro de la imagen).
- [ ] Variables en el panel de Render, sin enseñar los valores.
- [ ] Conclusiones: un límite real, coste de infra y de un turno, y el criterio de CI/CD (qué comprobaríais y cómo volvéis atrás).
- [ ] 3 fallos conocidos.

---

## Checklist del proyecto

- [ ] Repo GitHub desde el día 1 · PRs · `main` despliega
- [ ] Mismo dominio que el PB2 · agente reutilizado
- [ ] `/docs` en local y en Render
- [ ] `/ask` y `/approve` con el contrato (`auto_aprobar`, `pendiente_hitl`)
- [ ] Postgres local y Postgres de Render · historial tras redeploy
- [ ] 401 · 429 · 504 · logs con `thread_id` y `duration_ms`
- [ ] `Dockerfile` con `0.0.0.0` y `${PORT:-8000}` · RAG dentro
- [ ] Front contra la URL de Render: health, chat, historial, HITL
- [ ] URL de despliegue enviada al profesorado, para poder entrar
- [ ] README + `.env.example` + sin secretos
- [ ] Informe (dibujo, contrato, Postgres vs MemorySaver, prueba de vida, conclusiones de arquitectura/coste y de CI/CD, 3 fallos)
- [ ] Presentación ~10 min (**sólo se permite un vídeo por grupo**)
- [ ] Entrega hecha **antes del 26/11 a las 23:59**
- [ ] Presentación el **viernes 4/12, de 16:00 a 18:00**

---

## Criterios de evaluación

El proyecto se valora en **seis áreas**. La mayoría son de **equipo**; una es **individual** (aportación real en Git). Los porcentajes son el **peso sobre la nota**.

Las cinco áreas base suman el **100 %**: Desarrollo Técnico (35 %), Presentación (23 %), Git (17 %), Trabajo en equipo (15 %) y Memoria (10 %). Los **Extras** suman aparte, hasta un **+10 %** adicional.

### Desarrollo Técnico · equipo · 35 %

- **API:** contrato claro, Swagger usable, el agente del PB2 detrás de `/ask` y `/approve`.
- **Datos:** Postgres de verdad; el historial sobrevive a un redeploy.
- **Deploy:** una imagen, `PORT`, URL pública enviada al profesorado, secretos fuera del repo.
- **Front:** cliente HTTP de esa URL (health, chat, historial, HITL).
- **Robustez:** 401, tope de peticiones, timeout, logs sin secretos.

> Publicar `/ask` sin API key, guardar el historial solo en SQLite del portátil, o un front que importa el grafo, son errores graves.

> Los nombres de ficheros del enunciado son **orientativos**. Se evalúa el comportamiento: FastAPI, Swagger, PostgreSQL, Docker, Render y un front contra la URL pública.

### Presentación · equipo · 23 %

- Expresión oral clara y repartida.
- Demo del front **contra Render**, más Swagger de esa misma URL.
- Narrativa con hilo: PB1 (RAG) → PB2 (agente) → esta URL.

### Git · equipo · 17 %

- Repo limpio, README que lleva de cero a la URL, ramas/PRs, `main` desplegable.
- Sin secretos.

### Trabajo en equipo · individual · 15 %

Según historial Git: volumen, consistencia, calidad de commits/PRs, revisión de compañeras/os.

> Sin presencia objetiva en Git, esta área puede no superarse de forma individual.

### Memoria · equipo · 10 %

El informe cierra con conclusiones del sistema desplegado: arquitectura, un límite real, coste de infra y de un turno, y el criterio de CI/CD (qué se comprobaría, dónde viven los secretos, cómo se despliega y cómo se vuelve atrás). Contar el temario sin aplicarlo a su URL no puntúa.

### Extras · opcional · +10 %

Por ejemplo un CI con GitHub Actions, la abstención del RAG enseñada desde Swagger en la URL pública, multimodal desde el front, o un **uso sostenido de SDD**. Los extras **no** sustituyen los requisitos obligatorios.

**En resumen:** el agente del PB2 queda publicado. Swagger enseña el contrato, Postgres guarda el historial, Docker y Render lo sirven, y el front habla con esa URL.
