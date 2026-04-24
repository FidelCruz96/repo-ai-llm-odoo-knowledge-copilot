#!/usr/bin/env bash
set -euo pipefail

if ! command -v gcloud >/dev/null 2>&1; then
  echo "[ERROR] gcloud CLI no instalado."
  exit 1
fi

required_vars=(
  GCP_PROJECT_ID
  SERVICE_NAME
)

for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "[ERROR] Falta variable requerida: $var"
    exit 1
  fi
done

GCP_REGION="${GCP_REGION:-us-central1}"
AR_REPO="${AR_REPO:-odoo-copilot}"
IMAGE_NAME="${IMAGE_NAME:-odoo-knowledge-copilot}"
RUN_SA_EMAIL="${RUN_SA_EMAIL:-}"
INSTANCE_CONNECTION_NAME="${INSTANCE_CONNECTION_NAME:-}"

MODEL_NAME="${MODEL_NAME:-gpt-4o-mini}"
EMBEDDING_MODEL="${EMBEDDING_MODEL:-text-embedding-3-large}"
TOP_K="${TOP_K:-5}"
SIMILARITY_THRESHOLD="${SIMILARITY_THRESHOLD:-0.75}"
RATE_LIMIT_PER_MINUTE="${RATE_LIMIT_PER_MINUTE:-30}"
REQUEST_TIMEOUT_S="${REQUEST_TIMEOUT_S:-5}"
CHUNK_SIZE="${CHUNK_SIZE:-800}"
CHUNK_OVERLAP="${CHUNK_OVERLAP:-100}"
EMBEDDING_DIMENSIONS="${EMBEDDING_DIMENSIONS:-3072}"
REDIS_URL="${REDIS_URL:-}"
DEPLOY_SECRETS="${DEPLOY_SECRETS:-OPENAI_API_KEY=OPENAI_API_KEY:latest,API_KEY=API_KEY:latest,DATABASE_URL=DATABASE_URL:latest}"

IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${AR_REPO}/${IMAGE_NAME}:${GITHUB_SHA:-local}"

echo "[INFO] Building image: ${IMAGE_URI}"
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet
docker build -t "${IMAGE_URI}" .
docker push "${IMAGE_URI}"

echo "[INFO] Deploying Cloud Run service: ${SERVICE_NAME}"
deploy_cmd=(
  gcloud run deploy "${SERVICE_NAME}"
  --project "${GCP_PROJECT_ID}"
  --region "${GCP_REGION}"
  --image "${IMAGE_URI}"
  --platform managed
  --allow-unauthenticated
  --set-env-vars "APP_ENV=production,MODEL_NAME=${MODEL_NAME},EMBEDDING_MODEL=${EMBEDDING_MODEL},TOP_K=${TOP_K},SIMILARITY_THRESHOLD=${SIMILARITY_THRESHOLD},RATE_LIMIT_PER_MINUTE=${RATE_LIMIT_PER_MINUTE},REQUEST_TIMEOUT_S=${REQUEST_TIMEOUT_S},CHUNK_SIZE=${CHUNK_SIZE},CHUNK_OVERLAP=${CHUNK_OVERLAP},EMBEDDING_DIMENSIONS=${EMBEDDING_DIMENSIONS},REDIS_URL=${REDIS_URL}"
  --set-secrets "${DEPLOY_SECRETS}"
)

if [[ -n "${RUN_SA_EMAIL}" ]]; then
  deploy_cmd+=(--service-account "${RUN_SA_EMAIL}")
fi

if [[ -n "${INSTANCE_CONNECTION_NAME}" ]]; then
  deploy_cmd+=(--add-cloudsql-instances "${INSTANCE_CONNECTION_NAME}")
fi

"${deploy_cmd[@]}"

SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" --project "${GCP_PROJECT_ID}" --region "${GCP_REGION}" --format='value(status.url)')"
echo "[OK] Deploy complete: ${SERVICE_URL}"
