# Deployment

## Objetivo
Despliegue en GCP Cloud Run con imagen en Artifact Registry y base en Cloud SQL.

## Flujo CI/CD
1. `ci.yml`: lint, tests, coverage, seguridad, build Docker.
2. `deploy.yml`: build/push imagen + deploy Cloud Run + check `/v1/health`.

## Variables/secretos requeridos en GitHub
- `vars.GCP_PROJECT_ID`
- `vars.GCP_REGION`
- `vars.SERVICE_NAME`
- `vars.AR_REPO`
- `vars.RUN_SA_EMAIL` (recomendado)
- `vars.INSTANCE_CONNECTION_NAME` (si usas Cloud SQL)
- `secrets.GCP_WORKLOAD_IDENTITY_PROVIDER`
- `secrets.GCP_SERVICE_ACCOUNT`
- Secretos en GCP Secret Manager:
  - `OPENAI_API_KEY`
  - `API_KEY`
  - `DATABASE_URL`

## Deploy manual local
- Script: `scripts/deploy_cloud_run.sh`
- Requiere `gcloud` autenticado y variables de entorno configuradas.

## Estado actual
- Servicio desplegado: `odoo-knowledge-copilot`
- URL pública: `https://odoo-knowledge-copilot-376400137896.us-central1.run.app`
- Health cloud: `{"status":"healthy","checks":{"vector_store":"ok","llm_api":"ok","cache":"not_configured"}}`
