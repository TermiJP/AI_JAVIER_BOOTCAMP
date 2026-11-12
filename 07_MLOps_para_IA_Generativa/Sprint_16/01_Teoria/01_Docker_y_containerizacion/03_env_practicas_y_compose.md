![Cabecera](../../assets/cabecera_mlops.png)

# Env, buenas prácticas y Postgres al lado

## Variables de entorno

La app lee secrets y límites desde el entorno (`API_KEY`, `GEMINI_API_KEY`, `ASK_TIMEOUT_SECONDS`, `DATABASE_URL`, …). En Docker:

```bash
# una variable
docker run -e API_KEY=cambia-esta-clave -p 8000:8000 mi-api:local

# varias desde un archivo (local; no subir a git)
docker run --rm --name mi-api -p 8000:8000 --env-file .env mi-api:local
```

En la nube las mismas claves van en el **panel** del Web Service: la imagen no lleva secretos; el runtime sí.

Regla de oro: **código en git · secretos fuera**. El contenedor no cambia esa regla.

```env
# .env.example (idea)
API_KEY=
GEMINI_API_KEY=
ASK_TIMEOUT_SECONDS=300
DATABASE_URL=postgresql://postgres:123456@127.0.0.1:5432/postgres
```

---

## Buenas prácticas mínimas

| Práctica | Motivo |
|----------|--------|
| Imagen `slim` + `requirements.txt` | Reproducible y más ligera |
| `.dockerignore` con `.env`, `.git`, venv | No filtrar secrets ni hinchar la imagen |
| Un proceso principal = la API | Logs claros; el PaaS reinicia ese proceso |
| `/health` sin auth pesada | El hosting puede sondear el servicio |
| Rebuild tras cambiar código | La imagen es una **copia**; `run` no ve el editor |

Ciclo habitual al tocar código:

```bash
docker rm -f mi-api
docker build -t mi-api:local .
docker run --rm --name mi-api -p 8000:8000 --env-file .env mi-api:local
```

---

## Persistencia: el disco del contenedor es efímero

Al borrar el contenedor, se va lo escrito dentro (salvo volúmenes).

| Dato | Dónde vive en este sprint |
|------|---------------------------|
| Historial SQL | **PostgreSQL** (contenedor aparte o managed) |
| Guía / ficheros RAG | `COPY` dentro de la imagen de la API |
| Secrets | `-e` / `--env-file` / panel del PaaS |

---

## Postgres al lado (camino local)

Cuando hace falta historial, levantamos Postgres **aparte** con `docker run` (no hace falta Compose):

```bash
docker run --name mi-pg -e POSTGRES_PASSWORD=123456 -d -p 5432:5432 postgres
```

La API (en el PC o en otro contenedor) habla por `DATABASE_URL`. Detalle de host (`127.0.0.1` vs `host.docker.internal`) y pgAdmin → unidad de Postgres en cloud.

---

## Compose — solo mención

**Docker Compose** permite definir varios servicios en un YAML (API + DB). Existe y es útil en muchos equipos.

En este sprint el camino canónico es más simple:

- `docker build` / `docker run` de la API  
- `docker run` de Postgres cuando haga falta  
- en cloud: Web Service + Postgres managed (recursos separados)

No desplegamos Compose en el PaaS.

---

## Checklist

- [ ] Secretos por env, no en la imagen  
- [ ] `docker build` + `docker run` + `/health` OK  
- [ ] Si hay historial: Postgres en marcha y `DATABASE_URL` correcta  
