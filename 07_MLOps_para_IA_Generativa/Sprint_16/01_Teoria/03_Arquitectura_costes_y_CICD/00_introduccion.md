![Cabecera](../../assets/cabecera_mlops.png)

# Introducción — arquitectura/costes + CI/CD

Esta unidad tiene **dos bloques** cortos:

| Bloque | Pregunta |
|--------|----------|
| **3a** Arquitectura y costes | ¿Qué límites tiene lo que hemos desplegado y qué nos cuesta? |
| **3b** CI/CD | ¿Cómo evitamos “a mí me compilaba” en cada push? |

No montamos un diagrama enterprise ni un pipeline de 20 jobs. El objetivo es **leer** el sistema (API + PaaS + Postgres) con ojos de producción junior, y conocer la idea de **CI** (Actions: test + `docker build`).

```text
Imagen local ──► Servicio público
                         │
U3a entender límites ◄───┘
U3b Actions (teoría)
```
