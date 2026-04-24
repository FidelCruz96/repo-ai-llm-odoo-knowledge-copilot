# Security

## Controles implementados
- API key obligatoria para `/v1/query` y `/v1/ingest`
- rate limiting por minuto
- validación de extensión y tamaño en ingesta
- secretos fuera del repositorio mediante `.env` y Secret Manager
- trazabilidad básica con `trace_id`

## Evidencia
- reporte consolidado: `reports/security_scan.json`
- escaneo actual: `bandit=ok`, `pip-audit=ok`, `gitleaks=ok`
- validación de seguridad en código:
  - `app/core/security.py`
  - `app/core/rate_limit.py`
  - `app/utils/file_validation.py`
  - `app/services/rag_service.py`
  - `app/services/llm_service.py`

## Matriz de amenazas

| Amenaza | Vector | Control actual | Evidencia | Riesgo residual |
|---|---|---|---|---|
| Prompt injection | Preguntas que intentan forzar al modelo a ignorar el contexto | Prompt de sistema acotado y respuesta condicionada a contexto recuperado | `app/services/llm_service.py`, `app/services/rag_service.py` | Medio-Alto |
| Data leakage | Respuesta con información fuera del corpus o de filtros esperados | Respuesta basada en chunks recuperados y filtros por `module` o `doc_id` | `app/services/vector_service.py`, `app/services/rag_service.py` | Medio |
| Acceso no autorizado | Llamadas directas a endpoints sensibles sin credenciales | API key obligatoria en `/v1/query` y `/v1/ingest` | `app/core/security.py`, `app/api/routes_query.py`, `app/api/routes_ingest.py` | Medio |
| DoS / abuso de costo | Muchas requests por minuto o repetición maliciosa | rate limiting y timeouts configurables | `app/core/rate_limit.py`, `app/core/config.py` | Alto |
| Ingesta maliciosa | Subida de archivos vacíos, enormes o con extensión no permitida | Validación previa de extensión y tamaño | `app/utils/file_validation.py`, `app/api/routes_ingest.py` | Medio |
| Hallucinations | Consultas sin contexto suficiente o corpus insuficiente | Fallback explícito cuando no hay chunks confiables | `app/services/rag_service.py` | Medio |

## Riesgos residuales
- El rate limiting es en memoria y no distribuido.
- No hay WAF ni protección anti-bot avanzada.
- No existe pipeline formal de moderación o sanitización profunda del contenido documental.
- El sistema no cifra ni clasifica documentos a nivel de dominio de negocio dentro del repositorio.
