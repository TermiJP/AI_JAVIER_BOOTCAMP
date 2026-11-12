![Cabecera](../../../assets/cabecera_mlops.png)

# Workout: API segura + Docker

Vamos a trabajar con una **API FastAPI** ya segura (API key, rate limit, CORS) y un **cliente Streamlit**. Aquí el foco es **empaquetarla en un contenedor** y probarla en local. Posteriormente, la subiremos a la nube.

```text
cliente (Streamlit :8501) ──HTTP──► API en Docker (:8000)
     02_cliente_streamlit/              01_api_segura_crud_docker/
                                              ↑
                                         Dockerfile
```

## Estructura

```text
.
├── README.md                 # Esta guía
├── 01_api_segura_crud_docker/       # Servidor + Dockerfile
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── app.py
│   ├── security.py
│   ├── rate_limit.py
│   ├── config.py
│   ├── schemas.py
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
└── 02_cliente_streamlit/     # Cliente HTTP (opcional)
    ├── app.py
    ├── requirements.txt
    └── README.md
```

| Carpeta | Rol | Puerto típico |
|---------|-----|----------------|
| [`01_api_segura_crud_docker/`](./01_api_segura_crud_docker/) | Servidor (contenedor) | `8000` |
| [`02_cliente_streamlit/`](./02_cliente_streamlit/) | Cliente | `8501` |

---

## Qué probamos en el workout

1. Revisar que la API arranca en local (venv + uvicorn), como siempre.
2. Construir la **imagen** con `docker build`.
3. Arrancar el **contenedor** con `--env-file .env` (secretos en runtime, no dentro de la imagen).
4. Probar `/health` y `/items?api_key=...`.
5. (Opcional) Apuntar Streamlit al contenedor.
6. (Opcional) Desplegar el mismo `Dockerfile` en Render.

La API de negocio y la capa de seguridad **ya están dadas**. No reescribimos el CRUD: aprendemos a **empaquetarlo**.

---

## 1) API en local (sin Docker)

Útil para comprobar que el código responde antes del build.

```bash
cd 01_api_segura_crud_docker
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # editamos API_KEY
uvicorn app:app --reload --port 8000
```

- Health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Detalle de auth / rate limit / paginación: [`01_api_segura_crud_docker/README.md`](./01_api_segura_crud_docker/README.md).

---

## 2) Docker — build y run

Desde `01_api_segura_crud_docker/` (donde está el `Dockerfile`). Si aún no tenéis `.env`:

```bash
cp .env.example .env               # editamos API_KEY
```

```bash
docker build -t api-segura-crud .
docker run --rm --name api-segura -p 8000:8000 --env-file .env api-segura-crud
```

| Pieza | Por qué |
|-------|---------|
| `--name api-segura` | Nombre fijo del **contenedor** (si no, Docker inventa uno) |
| `-p 8000:8000` | Publicamos el puerto del contenedor en el host |
| `--env-file .env` | Secretos en **runtime** (mismo fichero que en local); no van dentro de la imagen |
| `.dockerignore` | Evita meter `.env`, `.venv`, `.git` en el build |

Comprobaciones (sustituid `<CLAVE>` por el `API_KEY` del `.env`):

- `GET http://127.0.0.1:8000/health` → **200** (sin clave)
- `GET http://127.0.0.1:8000/items` → **401**
- `GET http://127.0.0.1:8000/items?api_key=<CLAVE>` → **200**

El `CMD` del Dockerfile usa `${PORT:-8000}`: puerto **8000** por defecto; si existe la variable `PORT`, se usa esa.

### Alternativa: `-e` una a una

```bash
docker run --rm --name api-segura -p 8000:8000 \
  -e API_KEY=cambia-esta-clave \
  -e RATE_LIMIT_PER_MINUTE=10 \
  -e CORS_ORIGINS=http://127.0.0.1:8501,http://localhost:8501 \
  api-segura-crud
```

### Comandos útiles (terminal y Docker Desktop)

También podéis usar **Docker Desktop**: pestaña *Containers* / *Images* → Stop, Start (Play), Delete.

En terminal podéis usar el **nombre** (`api-segura`, `api-segura-crud`) **o el ID**. El ID lo veis con `docker ps` / `docker images`. Basta el **prefijo** del ID (p. ej. las 3 primeras cifras) **si es único** entre lo que tenéis listado; si hay ambigüedad, Docker se queja y hay que poner más caracteres.

```bash
# Listar contenedores en marcha
docker ps

# Listar todos (también parados)
docker ps -a

# Parar el contenedor (nombre, ID completo o prefijo)
docker stop api-segura
# docker stop a1b3c4d5e6f7
# docker stop a1b

# Arrancar un contenedor que está parado
docker start api-segura
# docker start a1b3c4d5e6f7
# docker start a1b

# Borrar el contenedor (tiene que estar parado)
docker rm api-segura
# docker rm a1b3c4d5e6f7
# docker rm a1b

# Listar imágenes
docker images

# Borrar la imagen (nombre:tag, ID completo o prefijo)
docker rmi api-segura-crud
# docker rmi c3d4e5f6a7b8
# docker rmi c3d
```

**Nota sobre `--rm`:** en el `docker run` de arriba usamos `--rm`. Al hacer `docker stop`, Docker **borra** el contenedor solo. En ese caso no hay `docker start`: hay que volver a `docker run`.  
Si queréis practicar stop → start, lanzad **sin** `--rm`:

```bash
docker run --name api-segura -p 8000:8000 --env-file .env api-segura-crud
```

---

## 3) Cliente Streamlit para conectarse a la API levantada con Docker

Con el contenedor en `:8000`:

```bash
cd 02_cliente_streamlit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env               # misma API_KEY que pasaste al contenedor
streamlit run app.py
```

**Listar con clave** → 200. **Sin clave** → 401.

---

## 4) Render para desplegar la API en la nube

1. Repo con `01_api_segura_crud_docker` como raíz del servicio (o monorepo apuntando a esa carpeta).
2. Web Service → **Docker**.
3. Environment: `API_KEY` (obligatoria); opcional `RATE_LIMIT_PER_MINUTE`, `CORS_ORIGINS`.
4. Render inyecta `PORT`; nuestro Dockerfile ya lo respeta.

Nunca subáis `.env` con secretos reales.

---

## Cómo leer el Dockerfile

```dockerfile
# Imagen base oficial de Python (ligera)
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt dentro del contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el código de la API dentro del contenedor
COPY . .

# Puerto documentado (hay que publicarlo con -p al hacer run)
EXPOSE 8000

# Puerto 8000 por defecto; si existe la variable PORT, se usa esa
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```

- `--host 0.0.0.0` → accesible desde fuera del contenedor.
- `${PORT:-8000}` → usa `PORT` si está definida; si no, 8000.
- `.dockerignore` → no metemos `.env`, `.venv`, `.git` en la imagen.

---

## Checklist

- [ ] `docker build` OK
- [ ] Contenedor: `/health` → 200
- [ ] `/items` sin `api_key` → 401; con `?api_key=` → 200
- [ ] Secretos por `-e` / panel; `.env` en `.dockerignore`
- [ ] Streamlit habla con el contenedor
- [ ] (Opcional) Deploy en Render con `API_KEY` en el panel
