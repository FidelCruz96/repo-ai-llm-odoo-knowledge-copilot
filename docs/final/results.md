# Resultados

## Estado funcional
- Endpoints implementados: `/v1/health`, `/v1/ingest`, `/v1/query`.
- Pipeline RAG operativo: ingesta -> retrieval -> generación.

## Evidencia técnica actual
- Cobertura > 60% (`79%`).
- Test de integración de pipeline incluido.
- Docker multi-stage y docker-compose con health checks.
- Makefile operativo con comandos principales.
- URL pública cloud operativa:
  - `https://odoo-knowledge-copilot-376400137896.us-central1.run.app`
- `reports/ragas_report.json` generado:
  - `cases_total=16`
  - `cases_failed=0`
  - `faithfulness=0.4115`
  - `answer_relevancy=0.1614`
  - `context_recall=0.5`
  - `context_precision=0.5`
- `reports/load_test_report.json` generado (k6, 10 VUs, 30s):
  - `p50 (med)=1853.61 ms`
  - `p95=2516.45 ms`
  - `p99=3512.79 ms`
  - `throughput=4.09 req/s`
  - `error_rate=0%`
- `reports/security_scan.json` generado:
  - `bandit=ok`
  - `pip-audit=ok`
  - `gitleaks=ok`
