# Testing

## Estrategia
- Unit tests para utilidades y servicios críticos.
- Test de integración de pipeline RAG en memoria.
- Cobertura automatizada con `pytest-cov`.

## Comandos
- `make test`
- `make coverage`

## Estado actual
- Suite: `35` tests passing.
- Cobertura total: `79%` (`coverage.xml`).

## Evidencia ejecutada
- API pública validada en Cloud Run:
  - `GET /v1/health` -> `healthy`
  - `POST /v1/ingest` -> `200`
  - `POST /v1/query` -> `200`
- RAGAS-style ejecutado y guardado en `reports/ragas_report.json`.
- k6 ejecutado con `10` VUs y guardado en `reports/load_test_report.json`.
