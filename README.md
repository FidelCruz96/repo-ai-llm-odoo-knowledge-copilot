# Odoo Knowledge Copilot

API RAG para consultas de documentación funcional y técnica de Odoo.

## Objetivo
- Ingerir documentos (`PDF`, `MD`, `TXT`).
- Indexarlos en PostgreSQL + pgvector.
- Responder preguntas con fuentes citadas.
- Medir latencia y trazabilidad mínima.

## Endpoints
- `GET /v1/health`
- `POST /v1/ingest`
- `POST /v1/query`

## Arquitectura resumida
- FastAPI (`app/`)
- Embeddings + LLM: OpenAI (`text-embedding-3-large`, `gpt-4o-mini`)
- Vector Store: PostgreSQL + pgvector
- Redis opcional para soporte operativo
- Docker Compose para entorno local

## Requisitos
- Python 3.12
- Docker + Docker Compose
- (Opcional) `k6`, `bandit`, `pip-audit`, `gitleaks`, `ruff`, `mypy`

## Variables de entorno
Base en [`.env.example`](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/.env.example):
- `OPENAI_API_KEY`
- `API_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `MODEL_NAME`
- `EMBEDDING_MODEL`
- `TOP_K`
- `SIMILARITY_THRESHOLD`
- `RATE_LIMIT_PER_MINUTE`
- `MAX_UPLOAD_SIZE_MB`

## Ejecución local
1. `make setup`
2. `cp .env.example .env` y ajustar valores reales.
3. `make up`
4. Validar salud: `make health`

## Ingesta de documentos
- Cargar todos los sample docs:
  - `make seed`
- Cargar archivos específicos:
  - `make ingest FILES='data/sample_docs/odoo_inventory_basics.md data/sample_docs/odoo_purchase_approvals.md' MODULE=inventory`

## Consulta de ejemplo
```bash
curl -s -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"¿Qué es un picking en Odoo?","stream":false}'
```

## Tests y cobertura
- `make test`
- `make coverage`

Resultado actual:
- `35 passed`
- cobertura total `79%`

## Evaluación y performance
- RAGAS-style proxy:
  - `make ragas`
  - salida: `reports/ragas_report.json`
- Load test k6:
  - `make load-test`
  - salida: `reports/load_test_report.json`

## Seguridad
- Escaneo consolidado:
  - `make security`
  - salida: `reports/security_scan.json`

## CI/CD
- CI: [`.github/workflows/ci.yml`](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/.github/workflows/ci.yml)
- Deploy: [`.github/workflows/deploy.yml`](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/.github/workflows/deploy.yml)

## Deploy cloud
- Script manual: [`scripts/deploy_cloud_run.sh`](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/scripts/deploy_cloud_run.sh)
- URL pública: `https://odoo-knowledge-copilot-376400137896.us-central1.run.app`

## Documentación final
- [stack-decision.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/stack-decision.md)
- [implementation.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/implementation.md)
- [testing.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/testing.md)
- [deployment.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/deployment.md)
- [security.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/security.md)
- [costs.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/costs.md)
- [results.md](/home/fidelcruz/Documentos/repo-ai-llm-odoo-knowledge-copilot/docs/final/results.md)

## Limitaciones conocidas
- El rate limiting actual es en memoria (no distribuido).
- El reporte de RAGAS usa métricas proxy (no `ragas` oficial todavía).
- El corpus cloud de demo es pequeño (sample docs), por lo que la calidad depende de ese alcance.
