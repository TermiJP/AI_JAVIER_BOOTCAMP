![Cabecera](../../assets/cabecera_mlops.png)

# Dockerfile y FastAPI

Un **Dockerfile** es el guion para construir la imagen. Para una API FastAPI, el mínimo razonable es:

```dockerfile
# Imagen base oficial de Python (ligera)
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Lectura línea a línea

| Instrucción | Por qué |
|-------------|---------|
| `FROM python:3.12-slim` | Base oficial, Python fijo, imagen más ligera |
| `WORKDIR /app` | Directorio de trabajo dentro del contenedor |
| `COPY requirements.txt` + `RUN pip …` | **Antes** de copiar todo el código → cache de deps |
| `COPY . .` | Código de la API |
| `EXPOSE 8000` | Documenta el puerto (hace falta `-p` al hacer `run`) |
| `CMD … --host 0.0.0.0 --port ${PORT:-8000}` | Escucha en todas las interfaces; 8000 por defecto o el valor de `PORT` |

El módulo `app:app` es `archivo:variable` (como en local con uvicorn).

**Nota:** la forma JSON `CMD ["uvicorn", …, "8000"]` **no** expande `${PORT}`. Por eso usamos la forma shell: el hosting puede inyectar `PORT`.

## `.dockerignore`

Evita meter archivos no necesarios en la imagen (y secretos):

```text
.git
.env
__pycache__
*.pyc
.venv
venv
*.db
.pytest_cache
```

**Nunca** copiar `.env` con claves reales a la imagen. Los secrets entran en **runtime** (`-e`, `--env-file`, o panel del PaaS).

## Build y prueba local

```bash
docker build -t mi-api:local .
docker run --rm --name mi-api -p 8000:8000 --env-file .env mi-api:local
```

Luego `GET /health` y, si la API lleva clave, rutas protegidas con `?api_key=…`.

## Multi-stage y HEALTHCHECK (solo idea)

- **Multi-stage:** construir en una imagen pesada y copiar a una slim. No es obligatorio; con `python:*-slim` + `pip` basta.
- **HEALTHCHECK** en Dockerfile: opcional. Lo importante es tener un endpoint `/health` ligero; el PaaS suele sondearlo desde su panel.
