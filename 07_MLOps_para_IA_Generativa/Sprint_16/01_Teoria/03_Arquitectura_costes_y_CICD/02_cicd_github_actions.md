![Cabecera](../../assets/cabecera_mlops.png)

# CI/CD con GitHub Actions

**CI** (Continuous Integration): en cada push/PR, una máquina de GitHub **clona el repo**, instala deps y corre checks.  
**CD** (Continuous Deployment/Delivery): si el check pasa, **desplegar** (o dejar un artefacto listo).

En bootcamp nos quedamos en la **idea**: CI con `pip` + `docker build`. El deploy a Render suele ser el **auto-deploy** del propio PaaS al hacer push a `main`.

## ¿Por qué nos importa?

| Sin CI | Con CI mínimo |
|--------|----------------|
| “En local pasaba” | Misma receta en cada push |
| Dockerfile roto descubierto en el PaaS | `docker build` falla **antes** en Actions |
| Regresión en `/health` o auth | Un test o script lo pilla |

## Pipeline mínimo (idea)

```yaml
# .github/workflows/ci.yml — esquema
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install
        run: |
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi

      # Opcional: tests
      # - run: pytest -q

      - name: Docker build
        run: |
          if [ -f Dockerfile ]; then
            docker build -t app:ci .
          fi
```

Así comprobamos que el servicio **al menos construye**.

## Secretos en Actions

Si algún test necesita claves:

- **GitHub → Settings → Secrets and variables → Actions**
- En el workflow: `env: GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}`

No imprimáis secrets en los logs. Para muchos checks basta mockear el LLM y usar una `API_KEY` de test.

## Relación con el PaaS

Patrones habituales (de menos a más):

1. **Push a main → auto-deploy** del PaaS; Actions solo valida.  
2. Actions hace build y, si pasa, dispara deploy (hook / API del PaaS).

En bootcamp, **(1) + CI de build** es suficiente.

## Qué no montamos

- Matrices de 5 versiones de Python  
- Escaneo de vulnerabilidades enterprise  
- Preview environments por PR  
