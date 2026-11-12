![Cabecera](../../assets/cabecera_mlops.png)

# De local a cloud

Poco a poco estamos preparando nuestra aplicación para que pueda desplegarse en un entorno de producción. En este sprint nos centramos en **seguridad, robustez y observabilidad** de la API en local. El siguiente sprint (S16) se centra en **empaquetar y publicar** en la nube (Docker + PaaS).

## Qué no cambia al subir a cloud

La instrumentación de S15 **no se tira** en S16:

```text
S15  logger.info(...)  →  consola de uvicorn
S16  mismo logger.info(...)  →  logs del Web Service en el panel del PaaS
```

Seguimos logueando `thread_id`, `duration_ms`, 401/429/504… Solo cambia **dónde leemos** esos mensajes: de la terminal al panel del proveedor.

Tampoco reinventamos auth: `API_KEY`, rate limit y timeouts viajan en el **`.env` del PaaS** (variables del servicio), no hardcodeados.

## Qué sí cambia

| Local | Cloud |
|-------|--------|
| `uvicorn` en el portátil | Contenedor / Web Service |
| `.env` en disco | Secrets en el panel del PaaS |
| Reinicio = Ctrl+C | Redeploy / restart del servicio |
| Solo nosotros llamamos | URL pública → más ruido y abuso posible |

Por eso S15 endurece **antes** de abrir la puerta: sin clave ni rate limit, una URL pública se gasta sola (tokens, CPU).

## Varios entornos (visión)

En un producto real suele haber al menos:

- **Desarrollo** — local o un deploy de prueba; logs verbosos, límites holgados.
- **Preproducción / staging** — casi como prod; mismos logs, datos de prueba.
- **Producción** — tráfico real; mismos patrones de log, secretos distintos, límites más estrictos.

No hace falta montar tres stacks de observabilidad. Lo habitual: **mismo código de logging**, distinta config (nivel, `API_KEY`, `ASK_TIMEOUT_SECONDS`, `RATE_LIMIT_PER_MINUTE`).

## Leer logs en producción

Cuando la API esté en la nube, el primer sitio al depurar sigue siendo el **log**: ¿401/429? ¿timeout 504? ¿falta un secreto en el panel? Misma lectura que en local; solo cambia la pantalla.

Los detalles del PaaS concreto (arrancar el servicio, panel, etc.) los veremos más adelante.

## Resumen

- S15: instrumentamos y endurecemos en local.
- S16: mismos logs, otra “pantalla” (panel del PaaS) + deploy.
- Entornos distintos = misma idea de observabilidad, distinta configuración.
- Observabilidad enterprise (APM, tracing distribuido) queda fuera del material.
