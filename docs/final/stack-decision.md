# Stack Decision (v1.0)

## Alcance final
- Caso de uso: consultas de documentación funcional/técnica de Odoo con RAG.
- In Scope v1.0: `/v1/health`, `/v1/ingest`, `/v1/query`, trazabilidad básica, seguridad mínima, pruebas, reportes y despliegue en Cloud Run.
- Out of Scope v1.0: UI web final, multi-tenant enterprise, fine-tuning, Kubernetes.

## Stack definitivo
- Backend: FastAPI + Uvicorn (Python 3.12 actual del repo).
- LLM: OpenAI `gpt-4o-mini`.
- Embeddings: OpenAI `text-embedding-3-large`.
- Vector Store: PostgreSQL + pgvector.
- Cache / soporte operacional: Redis (opcional).
- Infra local: Docker + Docker Compose.
- CI/CD: GitHub Actions.
- Cloud recomendada: GCP Cloud Run + Cloud SQL.

## KPIs principales
- `latency_p95_ms`: objetivo `< 3000`.
- `faithfulness`: objetivo `>= 0.85` (o proxy documentado si no se usa RAGAS oficial).
- `error_rate`: objetivo `< 1%`.
