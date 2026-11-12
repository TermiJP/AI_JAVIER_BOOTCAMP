![Cabecera](../../assets/cabecera_mlops.png)

# Seguridad de tools del agente

Esto **no** es el `?api_key=` de la API HTTP. Es lo que el **agente** puede hacer cuando elige una tool.

## Riesgos típicos

- Tool que llama a APIs externas sin timeout.
- Prompt o tool que acaba **filtrando** `GEMINI_API_KEY` o datos sensibles en la respuesta.
- Acciones irreversibles (borrar, pagar…) sin HITL.

## Prácticas mínimas

1. Timeout en cada tool / llamada HTTP.
2. No meter secretos en el estado que el LLM “ve”.
3. Allowlist mental: solo las tools que necesitamos en `src/tools/`.
4. HITL (`/approve`) cuando el plan sea sensible (ya lo vimos en S14).

No montamos un producto de “agent security” enterprise. Con estas reglas el agente ya no va a ciegas.

## Resumen

- Auth HTTP protege **quién llama**.
- Seguridad de tools del agente limita **qué hace** el grafo por dentro.
