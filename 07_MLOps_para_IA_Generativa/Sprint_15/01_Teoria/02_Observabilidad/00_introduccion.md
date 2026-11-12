![Cabecera](../../assets/cabecera_mlops.png)

# Introducción — Observabilidad

Sin señales, depurar un agente es adivinar:

```text
Cliente → 500
¿Fue la key? ¿El LLM? ¿Una tool? ¿Timeout?
```

Con observabilidad mínima respondemos mirando la **consola** (y luego los logs del PaaS). Buenos logs = depurar con evidencia, no a ciegas.

## Mapa de lectura

| # | Doc | Para qué |
|---|-----|----------|
| 1 | [Logs en local](./01_logs_en_local.md) | Logging, `thread_id`, `duration_ms` |
| 2 | [Agente y calidad](./02_agente_y_calidad.md) | Rastro del turno + checklist smoke |
| 3 | [De local a cloud](./03_de_local_a_cloud.md) | Misma instrumentación hacia S16 |

No montamos Prometheus ni LangSmith. Instrumentación **en código** + lectura humana de logs.

## Resumen

- Primero instrumentamos en local (S15).
- En S16, los mismos logs aparecen en el panel del PaaS.
