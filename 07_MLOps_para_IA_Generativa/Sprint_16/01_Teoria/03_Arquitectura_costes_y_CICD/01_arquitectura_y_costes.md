![Cabecera](../../assets/cabecera_mlops.png)

# Arquitectura y costes

## Mapa mental del sistema desplegado

```text
[Cliente: Postman / Streamlit local]
              │ HTTPS
              ▼
     ┌──────────────────┐
     │ PaaS Web Service │  ← FastAPI + agente + RAG (1 contenedor)
     │  API_KEY, rate,  │
     │  logs, timeout   │
     └────────┬─────────┘
              │ DATABASE_URL (si hay historial)
              ▼
     ┌──────────────────┐
     │ Postgres managed │
     └──────────────────┘

     Fuera: Gemini (tokens) · APIs externas
```

Una sola unidad de deploy para la app. La complejidad “de plataforma” (K8s, service mesh) **no entra**.

## Límites que vais a notar

| Límite | Efecto |
|--------|--------|
| **Cold start** (tier free) | Primera request tras dormir: varios segundos extra |
| **CPU / RAM** del plan | Agentes + embeddings pueden ir justos; 502/OOM si os pasáis |
| **Timeouts** | Los del PaaS + vuestro `ASK_TIMEOUT_SECONDS` |
| **Rate limit propio** | Protege abusos; también limita demos masivas |
| **Cuotas LLM** | 429 / facturación; independiente del hosting |

## Costes (dos facturas mentales)

1. **Infra** — Web Service + Postgres, dominio, etc.  
2. **Tokens / APIs** — cada `/ask` puede llamar al LLM y a tools externas.

En demos: modelos razonables, `ASK_TIMEOUT_SECONDS` holgado pero finito, y **siempre** `API_KEY` en el servicio público.

## Escalado (solo vocabulario)

| Idea | En este sprint |
|------|----------------|
| Vertical (más RAM/CPU) | Subir plan en el PaaS |
| Horizontal (más réplicas) | Existe en planes de pago; no lo montamos |
| Cola / workers | Fuera de alcance |

Un servicio estable + secrets + `/health` ya es un buen listón.
