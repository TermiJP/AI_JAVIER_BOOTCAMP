![Cabecera](../../assets/cabecera_mlops.png)

# PostgreSQL — local y cloud

Si la API guarda **historial** (conversaciones / turns), necesitamos una base de datos real. En este sprint usamos **PostgreSQL**:

1. **En el portátil** — contenedor Docker + pgAdmin (visor).
2. **En la nube** — Postgres managed (p. ej. Render) + `DATABASE_URL` en el panel.

```text
API (uvicorn o contenedor)
        │  DATABASE_URL
        ▼
 PostgreSQL (:5432)
        ▲
   pgAdmin (visor)
```

Sin `DATABASE_URL` la app **no arranca** (no hay fallback a fichero local).

---

## 1) Postgres en Docker (local)

Docker Desktop abierto:

```bash
docker run --name aire-pg -e POSTGRES_PASSWORD=123456 -d -p 5432:5432 postgres
```

| Pieza | Significado |
|-------|-------------|
| `--name aire-pg` | Nombre del contenedor (podéis usar otro) |
| `POSTGRES_PASSWORD=123456` | Contraseña del usuario `postgres` |
| `-p 5432:5432` | Puerto visible en el PC: `localhost:5432` |
| `-d` | En segundo plano |

Por defecto la BD se llama `postgres` (igual que el usuario).  
Comprobad: `docker ps` → debe aparecer el contenedor.

La password del contenedor debe coincidir con la de `DATABASE_URL`.

---

## 2) pgAdmin (visor)

1. Instalad [pgAdmin 4](https://www.pgadmin.org/download/).
2. **Add New Server**.
3. **General**: un nombre cualquiera.
4. **Connection**:

| Campo | Valor |
|-------|--------|
| Host name/address | `localhost` |
| Port | `5432` |
| Maintenance database | `postgres` |
| Username | `postgres` |
| Password | `123456` |

5. Save. Tras unos `/ask`, en esa BD aparecen tablas del historial (`conversation`, `message`).

---

## 3) `DATABASE_URL` — host vs contenedor

La API lee la URL desde el entorno:

```text
postgresql://postgres:123456@HOST:5432/postgres
```

| Dónde corre la API | `HOST` en la URL |
|--------------------|------------------|
| **uvicorn en el PC** | `127.0.0.1` (Postgres publicado en el host) |
| **API en Docker** (Windows/macOS) | `host.docker.internal` |

Dentro del contenedor de la API, `127.0.0.1` **no** es vuestro PC: por eso cambia el host.

Ejemplos:

```env
# API con uvicorn en el PC
DATABASE_URL=postgresql://postgres:123456@127.0.0.1:5432/postgres

# API en Docker (Windows/macOS)
DATABASE_URL=postgresql://postgres:123456@host.docker.internal:5432/postgres
```

`/health` debe devolver `"storage": "postgres"`.

**Importante:** a veces la nube entrega `postgres://…`. SQLAlchemy prefiere `postgresql://…`. En `config.py` normalizamos el prefijo si hace falta.

Las tablas se crean al arrancar (`create_all` / `ensure_schema`). No hace falta crearlas a mano en pgAdmin.

---

## 4) Postgres managed (cloud)

En un Web Service el disco del contenedor es **efímero**. El historial no puede vivir solo “dentro” de la imagen.

```text
FastAPI (Web Service)
        │  DATABASE_URL (Internal)
        ▼
PostgreSQL managed
```

Pasos típicos (Render u otro PaaS):

1. Crear un recurso **PostgreSQL** (misma región que el Web Service).
2. Copiar la **Internal Database URL** (desde el servicio web).
3. Pegarla como `DATABASE_URL` en Environment del Web Service.
4. Redeploy.
5. Probar `/health` → `"storage":"postgres"` y un `/ask` con clave.

Para mirar datos desde el PC con pgAdmin usad el host **externo** del panel (y SSL si lo pide el proveedor). Las tablas siguen creándose al arrancar la API.

---

## Resumen

| Entorno | Postgres | Cómo conecta la API |
|---------|----------|---------------------|
| Local | Contenedor `docker run` + pgAdmin | `127.0.0.1` o `host.docker.internal` |
| Cloud | Managed | Internal `DATABASE_URL` en el panel |

API **sin** historial SQL (p. ej. CRUD en memoria) puede vivir sin Postgres.  
Si hay turns / mensajes → **Postgres** desde el primer día de práctica.
