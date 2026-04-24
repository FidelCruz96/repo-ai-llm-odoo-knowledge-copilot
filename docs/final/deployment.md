# Deployment

## Objetivo
Desplegar la API en GCP Cloud Run usando una imagen almacenada en Artifact Registry y conectada a Cloud SQL mediante secretos de GCP.

## Workflows
- CI: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)
- Deploy: [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml)

## Variables requeridas

### Variables de GitHub Actions
- `vars.GCP_PROJECT_ID`
- `vars.GCP_REGION`
- `vars.SERVICE_NAME`
- `vars.AR_REPO`
- `vars.RUN_SA_EMAIL`
- `vars.INSTANCE_CONNECTION_NAME`

### Secretos de GitHub Actions
- `secrets.GCP_WORKLOAD_IDENTITY_PROVIDER`
- `secrets.GCP_SERVICE_ACCOUNT`

### Secretos consumidos en GCP
- `OPENAI_API_KEY`
- `API_KEY`
- `DATABASE_URL`

## Pasos exactos del deploy manual
1. Autenticar `gcloud`.
2. Exportar al menos `GCP_PROJECT_ID` y `SERVICE_NAME`.
3. Ajustar opcionalmente `GCP_REGION`, `AR_REPO`, `RUN_SA_EMAIL`, `INSTANCE_CONNECTION_NAME`.
4. Ejecutar `./scripts/deploy_cloud_run.sh`.
5. Obtener la URL del servicio desplegado.
6. Validar `GET /v1/health`.

## Script usado
- [`scripts/deploy_cloud_run.sh`](../../scripts/deploy_cloud_run.sh)

El script:
- construye la imagen Docker;
- publica la imagen en Artifact Registry;
- despliega Cloud Run;
- inyecta configuración por variables de entorno;
- conecta secretos desde Secret Manager;
- agrega Cloud SQL si `INSTANCE_CONNECTION_NAME` está definido.

## Configuracion observada del entorno
- servicio: `odoo-knowledge-copilot`
- revision lista mas reciente: `odoo-knowledge-copilot-00003-76c`
- URL actual: `https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app`
- Cloud SQL asociado: `odoo-kc-proyect:us-central1:odoo-kc-pg`
- autoscaling maximo observado: `20`

## Validacion final
Comprobacion esperada:
```bash
curl -fsS https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app/v1/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "checks": {
    "vector_store": "ok",
    "llm_api": "ok",
    "cache": "not_configured"
  }
}
```
