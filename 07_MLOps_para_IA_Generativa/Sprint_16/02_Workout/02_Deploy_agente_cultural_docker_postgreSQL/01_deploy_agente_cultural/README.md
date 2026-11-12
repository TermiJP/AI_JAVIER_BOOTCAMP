![Cabecera](../../../assets/cabecera_mlops.png)

# Workout: agente cultural + Docker + Postgres

La **API/agente ya vienen dados**. Aquí empaquetamos, persistimos en **Postgres** (con **pgAdmin** como visor) y, si da tiempo, desplegamos en la nube.

```text
cliente (opcional: Streamlit :8501)
        │
        ▼
API (uvicorn en el PC)  ──localhost:5432──►  PostgreSQL (contenedor Docker)
                                                   ▲
                                              pgAdmin (visor)
```

## Estructura

```text
.
├── README.md
├── 01_api_agente_segura_docker_postgreSQL/     # API + agente + Dockerfile (guía completa)
└── 02_cliente_streamlit/                       # Cliente HTTP opcional
```

| Carpeta | Rol |
|---------|-----|
| [`01_api_agente_segura_docker_postgreSQL/`](./01_api_agente_segura_docker_postgreSQL/) | Servidor — **empezad aquí** |
| [`02_cliente_streamlit/`](./02_cliente_streamlit/) | Cliente opcional |

## Qué hacemos

1. Levantar **PostgreSQL** en Docker + conectar **pgAdmin** (`localhost`).
2. Arrancar la API con **uvicorn** y `DATABASE_URL` a `127.0.0.1`.
3. Probar `/health`, `/ask`, ver historial en pgAdmin.
4. (Opcional) Empaquetar la API en Docker; (opcional) Streamlit; (opcional) Render.

Detalle de comandos, `.env` y checklist: [`01_api_agente_segura_docker_postgreSQL/README.md`](./01_api_agente_segura_docker_postgreSQL/README.md).

**No es entregable**; hay vídeo demo en clase.
