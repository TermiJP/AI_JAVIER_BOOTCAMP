![Cabecera](../../assets/cabecera_mlops.png)

# Introducción — Seguridad y robustez

En S14 nos centramos en crear una API con un CRUD de prueba. En este Sprint nos centraremos en añadir seguridad y robustez a la API.

```text
Sin protección:  cualquiera llama a POST /ask  →  gasto de tokens + datos
Con protección:  solo quien tiene la clave  →  controlamos el uso
```

Durante este Sprint nos centraremos en responder a esta pregunta: **¿quién puede llamar y qué pasa si algo va mal?**

## Mapa de lectura

| # | Doc | Para qué |
|---|-----|----------|
| 1 | [Autenticación y secrets](./01_autenticacion_y_secrets.md) | Claves, API key / JWT / OAuth, `Depends` |
| 2 | [Rate, timeouts y errores](./02_rate_timeouts_y_errores.md) | 429, 504, códigos claros |
| 3 | [Seguridad de tools del agente](./03_seguridad_de_tools_del_agente.md) | Qué puede hacer el grafo por dentro |

## Resumen

- Nos centramos en una capa de seguridad y robustez antes de llevar la API a producción.
- Seguridad ≠ “poner HTTPS” (eso llega con el PaaS en S16).
- Aquí: **quién entra**, **cuántas veces**, **cuánto tarda**, **qué ve el cliente si falla**.
