![Cabecera](../../assets/cabecera_mlops.png)

# Introducción — ¿por qué Docker?

Hasta ahora la API corre en **nuestro entorno**: Python del sistema o un venv, dependencias instaladas a mano, rutas que “funcionan en mi máquina”.

En cloud (y en el equipo del compañero) eso se rompe:

- otra versión de Python
- paquetes que faltan o chocan
- paths distintos (`C:\...` vs `/app/...`)
- “pero a mí me iba”

**Docker** empaqueta **código + runtime + dependencias** en una **imagen**. Al **ejecutar** esa imagen nace un **contenedor**: un proceso aislado con todo lo que necesita.

```text
Código FastAPI
    + requirements.txt
    + Python / sistema base
        → imagen Docker
            → contenedor (local o PaaS)
```

## Qué conseguimos

| Sin Docker | Con Docker |
|------------|------------|
| “En mi PC sí” | Misma imagen en local y en cloud |
| Instalar deps a mano en el servidor | `docker build` + `docker run` |
| Dudas de versión de Python | La imagen fija la base |

## Mapa de esta unidad

1. Imagen vs contenedor · ciclo `build` / `run`
2. Dockerfile mínimo para FastAPI
3. Secrets en runtime · buenas prácticas · Postgres al lado

## Qué no es Docker

- No sustituye la **seguridad de aplicación** (API key, rate limit): eso sigue en el código.
- No es **Kubernetes** ni orquestación de flotas: aquí un servicio (y, si hace falta, Postgres aparte).
- No “despliega solo”: el deploy lo hacemos en la unidad de cloud (PaaS).
