# Resultados

## Estado funcional
La solucion cumple el objetivo principal del MVP: demostrar una arquitectura RAG operativa, desplegada y medible para consultas sobre documentacion de Odoo.

Endpoints implementados:
- `GET /v1/health`
- `POST /v1/ingest`
- `POST /v1/query`

## Evidencia tecnica consolidada
- suite automatizada: **38 tests passing**
- cobertura total: **84%**
- despliegue cloud validado: `https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app`
- reporte RAGAS-style: `reports/ragas_report.json`
- reporte de seguridad: `reports/security_scan.json`

## Operacion normal del MVP

### Pipeline y contrato
El MVP sí valida:
- ingesta documental
- chunking y embeddings
- retrieval vectorial con filtros basicos
- generacion con LLM
- respuesta con fuentes
- trazabilidad basica con `trace_id`
- despliegue reproducible y CI/CD

### Evaluacion RAGAS-style
Resultados actuales:
- `cases_total=20`
- `cases_failed=0`
- `faithfulness=0.3792`
- `answer_relevancy=0.1663`
- `context_recall=0.5`
- `context_precision=0.5`

Lectura:
- el pipeline responde y cita fuentes, pero la calidad de retrieval todavia es base de MVP;
- los valores actuales sirven como linea base medible, no como techo de calidad del sistema.

### Prueba base del MVP
Archivo: `reports/load_test_report_10vus_local.json`

Condiciones:
- `10` VUs
- `60s`
- entorno local

Resultados:
- `p50=1726.88 ms`
- `p95=3005.60 ms`
- `p99=3312.68 ms`
- `throughput=4.09 req/s`
- `error_rate=0.78%`

Interpretacion:
- esta prueba representa la operacion normal evaluada del MVP;
- la tasa de error es baja;
- el `p95` queda cerca del objetivo de `3000 ms`, por lo que el sistema es viable para demostracion, pero todavia requiere optimizacion.

## Stress test
Archivo: `reports/load_test_report_50vus.json`

Condiciones:
- `50` VUs
- `60s`
- entorno Cloud Run

Resultados:
- `p50=205.97 ms`
- `p95=3363.01 ms`
- `p99=4085.16 ms`
- `throughput=47.45 req/s`
- `error_rate=89.40%`

Interpretacion obligatoria:
- esta prueba **no debe presentarse como rendimiento normal**;
- el resultado expone el **limite operativo** del entorno actual;
- el `p50` queda sesgado por respuestas fallidas rapidas y por eso no describe la experiencia real de solicitudes exitosas;
- durante esa validacion se observo estado `degraded` con `vector_store=error`, lo que confirma que el entorno entro en una zona no objetivo de operacion.

## Lo que el MVP valida y lo que no

### Si valida
- viabilidad funcional end-to-end
- arquitectura defendible para un primer release
- automatizacion basica de pruebas, seguridad y despliegue

### No valida aun
- calidad RAG optimizada
- estabilidad bajo concurrencia alta
- operacion distribuida con rate limiting robusto
- gobierno documental avanzado o multi-tenant

## Conclusion tecnica
El proyecto ya demuestra un MVP funcional, reproducible y desplegado. La arquitectura es valida para entrega final siempre que se presente con honestidad tecnica: operacion moderada aceptable, stress test como limite y calidad RAG aun en fase base.
