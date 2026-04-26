# Odoo Knowledge Copilot

API RAG para consultas de documentación funcional y técnica de Odoo.

## Objetivo
- Ingerir documentos `PDF`, `MD` y `TXT`.
- Indexarlos en PostgreSQL + pgvector.
- Responder preguntas con fuentes citadas.
- Medir latencia y trazabilidad mínima.

## Endpoints
- `GET /v1/health`
- `POST /v1/ingest`
- `POST /v1/query`

## Arquitectura resumida
- Backend: FastAPI en `app/`
- Pipeline RAG: servicios propios en Python (`embedding`, `vector`, `rag`, `llm`, `ingest`)
- LLM y embeddings: OpenAI (`gpt-4o-mini`, `text-embedding-3-large`)
- Vector store: PostgreSQL + pgvector
- Infra local: Docker Compose
- Deploy cloud: Cloud Run + Cloud SQL

## Requisitos
- Python 3.12
- Docker + Docker Compose
- Dependencias opcionales locales para validaciones: `k6`, `bandit`, `pip-audit`, `gitleaks`, `ruff`, `mypy`

> Nota:
> - En entorno local, `gitleaks` puede omitirse y el escaneo se reportará como warning.
> - En CI, `gitleaks` sí forma parte del pipeline obligatorio.

## Variables de entorno
Base en [`.env.example`](.env.example):
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

## Ejecucion local
1. `make install`
2. Ajustar `.env` si necesitas valores distintos a `.env.example`
3. `make dev`
4. `make health`

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

## Resultado actual
- Suite automatizada: `38 passed`
- Cobertura total: `84%`
- URL cloud validada: `https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app`
- Latencia local base: `p95=3005.60 ms` con `10` VUs durante `60s`
- Stress test: `50` VUs en Cloud Run con `89.40%` de error; se documenta como límite operativo, no como benchmark normal

## Comandos principales
- `make test`
- `make coverage`
- `make ragas`
- `make load-test`
- `make security`
- `make check-files`
- `make pre-delivery`

## Artefactos para evaluacion
- Arquitectura: [`docs/architecture/`](docs/architecture/)
- ADRs: [`docs/adr/`](docs/adr/)
- OpenAPI: [`docs/api/openapi.yaml`](docs/api/openapi.yaml)
- Documento maestro final: [`docs/final/AI_LLM_Project_Template_Filled.md`](docs/final/AI_LLM_Project_Template_Filled.md)
- Cobertura: [`reports/coverage.xml`](reports/coverage.xml)
- Reporte RAGAS-style: [`reports/ragas_report.json`](reports/ragas_report.json)
- Notebook de evaluacion: [`notebooks/evaluation.ipynb`](notebooks/evaluation.ipynb)
- Dataset de evaluacion: [`notebooks/eval_dataset.json`](notebooks/eval_dataset.json)
- Checklist estructural: [`REQUIRED_FILES.md`](REQUIRED_FILES.md)

## Documentacion final complementaria
- [`docs/final/stack-decision.md`](docs/final/stack-decision.md)
- [`docs/final/implementation.md`](docs/final/implementation.md)
- [`docs/final/testing.md`](docs/final/testing.md)
- [`docs/final/deployment.md`](docs/final/deployment.md)
- [`docs/final/security.md`](docs/final/security.md)
- [`docs/final/costs.md`](docs/final/costs.md)
- [`docs/final/results.md`](docs/final/results.md)

## Limitaciones conocidas
- El rate limiting actual es en memoria y no distribuido.
- El reporte de RAGAS usa métricas proxy, no la librería oficial `ragas`.
- El corpus de demostración es pequeño y curado; la calidad depende de ese alcance.
- El pipeline actual es suficiente para MVP, pero todavía no está optimizado para alta concurrencia.


## Demo final

Video de presentación: [Ver demo final] https://drive.google.com/file/d/1rGfkKudLz83eJFw8Out9ACyyAVG9LdBV/view?usp=sharing