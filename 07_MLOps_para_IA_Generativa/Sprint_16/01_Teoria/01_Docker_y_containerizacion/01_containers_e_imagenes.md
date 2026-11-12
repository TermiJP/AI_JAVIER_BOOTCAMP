![Cabecera](../../assets/cabecera_mlops.png)

# Containers e imágenes

## Imagen vs contenedor

| Concepto | Analogía | Qué es |
|----------|----------|--------|
| **Imagen** | Receta / plantilla | Capas de archivos + metadatos (qué comando arranca) |
| **Contenedor** | Plato servido | Proceso en marcha creado **desde** una imagen |

```bash
docker build -t mi-api:local .
# → crea/actualiza la imagen mi-api:local

docker run --rm --name mi-api -p 8000:8000 --env-file .env mi-api:local
# → arranca un contenedor; al salir (--rm) se borra el contenedor, no la imagen
```

Podemos lanzar **varios contenedores** de la misma imagen.

## Contenedor vs máquina virtual

| | Contenedor | VM |
|--|------------|-----|
| Sistema | Comparte el kernel del host | Kernel propio (más pesado) |
| Arranque | Segundos | Minutos a menudo |
| Aislamiento | Procesos / filesystem / red | Máquina completa |
| Uso típico aquí | Empaquetar **una app** (FastAPI) | No lo usamos |

Basta con **imagen = paquete reproducible** y **contenedor = proceso**.

## Ciclo mínimo

```text
Dockerfile  →  docker build  →  imagen
                                 ↓
                            docker run  →  contenedor (API escuchando)
```

### Comandos que usaremos

```bash
docker build -t nombre:tag .
docker images              # listar imágenes
docker run ...
docker ps                  # contenedores en marcha
docker ps -a               # también los parados
docker logs <nombre-o-id>  # salida de la app
docker stop <nombre-o-id>
docker start <nombre-o-id>
docker rm <nombre-o-id>
docker rm -f <nombre-o-id> # para y borra (útil antes de rebuild)
```

**Nota `--rm`:** al hacer `stop`, el contenedor se borra. Para practicar stop→start, lanzad sin `--rm`.

## Puertos

Dentro del contenedor la API escucha en `8000`. Para llegar desde el host:

```bash
docker run -p 8000:8000 mi-api:local
#          host:contenedor
```

Abrimos `http://127.0.0.1:8000/docs` en el navegador del host.

## Capas (idea)

Cada instrucción del `Dockerfile` (`FROM`, `COPY`, `RUN pip install`…) suele crear una **capa**. Si solo cambia el código y no el `requirements.txt`, Docker puede **reutilizar** la capa de `pip install` → builds más rápidos. Por eso el orden del Dockerfile importa (siguiente doc).
