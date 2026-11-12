![Cabecera](../../assets/cabecera_mlops.png)

# RAG en el contenedor

El RAG (guía cultural, guía de calidad del aire, etc.) vive **en el mismo proceso** que FastAPI: tool que lee ficheros / índice en memoria o en disco de la app.

Eso **no cambia** al desplegar.

```text
┌─────────────────────────────────────┐
│  Contenedor / Web Service           │
│  ┌─────────────────────────────┐    │
│  │ FastAPI                     │    │
│  │  · /ask + auth + rate       │    │
│  │  · grafo / agente           │    │
│  │  · tools (API externa, …)   │    │
│  │  · tool RAG (misma imagen)  │    │
│  │       ↑                     │    │
│  │  data/*.txt (COPY)          │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## Por qué no un “RAG Service” aparte

| Enfoque | Cuándo tiene sentido |
|---------|----------------------|
| **RAG dentro del API** (este sprint) | Un producto, un deploy, demos de bootcamp |
| Microservicio RAG / vector DB cloud | Equipos grandes, índices enormes, multi-tenant |

Montar un segundo servicio solo para “decir que hay cloud RAG” añade coste y superficie sin cambiar el aprendizaje de deploy.

## Qué va en la imagen

- Código del tool RAG  
- Ficheros fuente (`data/guia_….txt`, PDFs pequeños) vía `COPY` en el Dockerfile  
- Dependencias en `requirements.txt`

Al arrancar, el índice se puede **construir en startup** (si es ligero) o cargar desde artefactos en `data/`.

## Límites a tener en cuenta

- Imagen más grande si metéis muchos PDFs.
- Rebuild si cambia el corpus (nuevo `COPY` → nuevo deploy).
- Memoria del plan free: índices enormes en RAM pueden petar el servicio.

Con corpus **pequeño** (guías de demo) cabe sin drama.

## Resumen

**Un deploy = un contenedor FastAPI** que ya incluye agente + RAG.  
Postgres (siguiente doc) es para **historial SQL**, no para sustituir el RAG.