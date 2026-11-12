![Cabecera](../../assets/cabecera_mlops.png)

# Autenticación y secrets

**Autenticación** = demostrar *quién* llama. **Autorización** = qué puede hacer ese quien. Aquí nos centramos en autenticar la llamada a nuestra API y en dónde viven las claves.

## Secrets y variables de entorno

Durante todo el curso ya usábamos `.env` para cosas como `GEMINI_API_KEY`. En este Sprint aparece **otra** clave distinta: nuestra `API_KEY` para proteger la API.

### Dos claves, dos roles

| Variable | Quién la usa | Para qué |
|----------|--------------|----------|
| `GEMINI_API_KEY` | Nuestra app → Gemini | Llamar al LLM |
| `API_KEY` | Cliente → nuestra API | Demostrar que “puede” usar `/items` o `/ask` |

La clave de Gemini **nunca** se manda al navegador ni se pone en Swagger. Sí enviamos la `API_KEY` desde un cliente HTTP (Swagger, Postman, Streamlit, etc.).

### Reglas rápidas

1. Secretos solo en **entorno** (`.env` local; panel del PaaS en S16).
2. Subimos `.env.example` **sin** valores reales.
3. `.env` en `.gitignore`.
4. Si falta `API_KEY` al arrancar → mejor **fallar claro** (503) que dejar la API abierta “por defecto”.

```env
# .env.example
API_KEY=
RATE_LIMIT_PER_MINUTE=30
```

## Mapa de estrategias

| Estrategia | Idea en una frase |
|------------|-------------------|
| **API key** | Secreto compartido en cada request — **lo que usamos en este sprint** |
| **JWT** | Token firmado tras un login |
| **OAuth 2** | “Entra con Google / empresa” — acceso delegado |
| **Sesión / cookie** | Login clásico en web con cookie |

No hace falta implementarlas todas: en clase necesitamos **proteger la API** con poco código.

## API key

Es el mecanismo que **practicamos** en este sprint. Idea: quien conoce el secreto puede llamar; quien no, no.

### Qué es

Una **API KEY** es una cadena aleatoria que **nosotros** definimos y guardamos en el servidor. El cliente la manda en cada petición. El servidor compara: si coincide, deja pasar; si no, responde **401**.

No es un login de usuario humano. Es un “pase” para **servicios o herramientas**: Postman, Streamlit, otro backend, un alumno en `/docs`, etc.

```text
Cliente  →  request + api_key  →  nuestra API
                ↓
         ¿Coincide con API_KEY del .env?
           sí → 200 / lógica normal
           no → 401
```

### Dónde vive

- En el servidor: variable de entorno `API_KEY` (arriba).
- En el cliente: la misma cadena, en su `.env` o en Swagger/Postman/Streamlit.
- **Nunca** en el código fuente ni en el repo.

Ojo: `API_KEY` ≠ `GEMINI_API_KEY`.

### Cómo la enviamos

En este sprint usamos **query param**:

```http
GET /items?api_key=mi-clave-de-ejemplo
```

Misma idea por **header**:

```http
GET /items
Authorization: Bearer mi-clave-de-ejemplo
```

o `X-API-Key: …`. En producción a menudo se prefiere el header (la clave no queda en URLs ni en logs de proxy). Aquí priorizamos query por comodidad pedagógica.

### Una clave o varias

En clase basta **una** `API_KEY` compartida. En un producto real suele haber **una por cliente** — para rotar o revocar sin tumbar a todos. El rate limit ya piensa “por clave”.

Si cada cliente tuviera su API KEY, esta debería ser única y almacenada en la base de datos (p. ej. columna en usuarios).

### Qué responde el servidor

| Situación | Código típico |
|-----------|----------------|
| Clave correcta | Sigue el endpoint |
| Ausente o incorrecta | **401** |
| `API_KEY` no configurada en el servidor | **503** |

No devolvemos en el JSON el valor de la clave ni un stack trace. En logs tampoco escribimos `api_key=...` con el secreto.

### Límites de la API key

- No sustituye HTTPS en internet abierto — eso llega con el PaaS en S16.
- No da identidad ni roles por usuario; para eso irían JWT u OAuth.
- Si se filtra, hay que **cambiar** la clave en el `.env` y avisar a quien la usaba.
- Va de la mano del **rate limit**: la key dice *quién puede*; el límite dice *cuántas veces*.

Para leer más:

- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) — *API Keys* y *Sensitive information in HTTP requests*.
- [OWASP API Security — Broken User Authentication](https://github.com/OWASP/API-Security/blob/master/editions/2019/en/0xa2-broken-user-authentication.md) — la API key autentica al **cliente/app**, no al usuario humano.

## JWT

Un JWT (*JSON Web Token*, [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)) es un formato compacto para llevar datos firmados entre cliente y servidor. Se usa mucho tras un **login**.

### Tres partes

El token va en Base64URL, con tres trozos separados por `.` (`header.payload.signature`):

1. **Header** — tipo de token y algoritmo, por ejemplo `HS256`.
2. **Payload** — *claims*: `sub` (usuario), `exp` (caducidad), roles…
3. **Signature** — firma con una clave secreta; el servidor comprueba que nadie ha tocado el token.

El servidor **verifica la firma** y la caducidad. No es “comparar una única API key fija” como en nuestro hands-on.

Para verlo en vivo: abrimos [jwt.io](https://www.jwt.io/), pegamos un token de ejemplo y miramos header, payload y firma en el debugger.

### Flujo típico

```text
1. Cliente envía usuario/contraseña o usa OAuth
2. Servidor valida → genera JWT firmado
3. Cliente guarda el token (memoria, cookie httpOnly…)
4. En cada request: Authorization: Bearer <jwt>
5. Servidor valida firma + exp → deja pasar o 401
```

### Ventajas y cuidados

| Bien | Cuidado |
|------|--------|
| Compacto; encaja en header | Proteger la **clave de firma** |
| Sin estado en el servidor | Poner **`exp`**; renovar / refresh |
| Claims útiles (roles) | Siempre **HTTPS** en tránsito |

Aquí **no** montamos login + front + JWT: el tiempo no compensa el objetivo de proteger la API de negocio.

Para leer más:

- [Auth0 — JWT structure](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-structure)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html)

## OAuth 2

OAuth 2 es un protocolo de **autorización**: una app obtiene permiso para acceder a recursos en nombre del usuario **sin** quedarse con su contraseña. En la práctica es el “Entra con Google / GitHub / empresa”.

Nuestra app recibe un **access token** — a menudo un JWT — y lo usa contra la API del proveedor o contra la nuestra. Útil con **usuarios humanos** y SSO. Aquí no lo implementamos.

Para leer más:

- [OAuth 2.0 — oauth.net](https://oauth.net/2/)
- [What is OAuth 2.0? — Auth0](https://auth0.com/intro-to-iam/what-is-oauth-2)
- [FAQ OAuth — oauth.net](https://oauth.net/faq/) — OAuth no es autenticación por sí solo; para identidad se usa OpenID Connect encima.

## Por qué elegimos API key aquí

| Criterio | API key | JWT / OAuth |
|----------|---------|-------------|
| Proteger API de IA entre servicios | Sí | Posible, más complejo |
| Probar en `/docs` sin front | Fácil | Incómodo |
| Tiempo de clase junior | Bajo | Alto |
| Usuarios humanos con sesión | Limitado | Mejor encaje |

**Regla:** API key para el contrato servidor↔servidor o para una demo. JWT u OAuth cuando haya producto con usuarios y UI de login.

## Protección de endpoints

No todas las rutas deben pedir clave.

| Ruta | ¿Clave? | Motivo |
|------|---------|--------|
| `GET /docs`, `GET /openapi.json` | No | Documentación / aprendizaje |
| `GET /health` | No | Pulso del servicio (monitores, PaaS…) |
| `GET/POST/PUT/DELETE /items` | **Sí** | Negocio |
| `POST /ask`, `POST /approve` | **Sí** | Agente |

### Patrón en FastAPI: `Depends`

```python
from fastapi import Depends, Query, HTTPException

def require_api_key(api_key: str | None = Query(default=None)):
    if not settings.API_KEY:
        raise HTTPException(status_code=503, detail="API_KEY no configurada")
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida o ausente")
    return api_key

@app.get("/items", dependencies=[Depends(require_api_key)])
def list_items(...):
    ...
```

Al abrir `http://127.0.0.1:8000/docs` (Swagger), en una ruta protegida aparece el campo **`api_key`**. Pulsamos *Try it out*, escribimos el valor del `.env` y *Execute*: Swagger manda `?api_key=...`. Correcta → 200; falta o falla → 401.

## Resumen

- `API_KEY` ≠ `GEMINI_API_KEY`; secretos solo en entorno.
- Hands-on: **API key** por query + `Depends`; JWT/OAuth solo idea.
- `/health` y `/docs` abiertos; el resto cerrados.
