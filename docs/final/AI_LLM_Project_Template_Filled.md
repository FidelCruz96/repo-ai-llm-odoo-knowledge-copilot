# AI LLM Project Template Filled

## 1. Resumen ejecutivo
Odoo Knowledge Copilot es una API RAG orientada a consultas funcionales y tecnicas sobre documentacion de Odoo. El sistema ingiere documentos, genera embeddings, recupera contexto relevante desde PostgreSQL + pgvector y responde en lenguaje natural usando OpenAI, devolviendo ademas fuentes y `trace_id`.

El proyecto ya valida un MVP funcional de punta a punta: API, seguridad basica, almacenamiento vectorial, evaluacion RAGAS-style proxy, pruebas automatizadas, reportes de seguridad y despliegue en Cloud Run.

## 2. Problema y oportunidad
En equipos que trabajan con Odoo, el conocimiento funcional y tecnico suele estar fragmentado entre manuales, procedimientos, tickets y notas internas. Esto incrementa tiempos de busqueda, dependencia de expertos y respuestas inconsistentes. El proyecto aborda ese problema con una interfaz de consulta unificada sobre un corpus documental curado.

## 3. Requerimientos

### Requerimientos funcionales principales
- ingesta documental por API
- consultas en lenguaje natural en espanol
- retrieval semantico previo a la generacion
- respuestas con fuentes
- endpoint de salud
- autenticacion por API key

### Requerimientos no funcionales principales
- despliegue reproducible con Docker
- cobertura automatizada y tests de regresion
- trazabilidad basica por request
- seguridad minima de secretos y control de acceso
- latencia funcional en entorno MVP

## 4. Arquitectura

### Stack final
- Backend: FastAPI + Uvicorn
- Orquestacion RAG: pipeline propio en Python
- LLM: OpenAI `gpt-4o-mini`
- Embeddings: OpenAI `text-embedding-3-large`
- Vector store: PostgreSQL + pgvector
- Infra local: Docker Compose
- Cloud: Cloud Run + Cloud SQL

### Componentes principales
- `app/api/`: rutas HTTP
- `app/services/embedding_service.py`: embeddings
- `app/services/vector_service.py`: indexacion y retrieval en pgvector
- `app/services/llm_service.py`: generacion con OpenAI
- `app/services/rag_service.py`: orquestacion de consulta
- `app/services/ingest_service.py`: pipeline de ingesta

### Diagramas
- contexto: `docs/architecture/c4-contexto.png`
- contenedores: `docs/architecture/c4-contenedores.png`
- secuencia: `docs/architecture/secuencia-query.png`

## 5. Decisiones arquitectonicas
- ADR LLM: `docs/adr/ADR-001-llm-base.md`
- ADR vector store: `docs/adr/ADR-002-vector-store.md`
- ADR orquestacion RAG: `docs/adr/ADR-003-rag-orchestration.md`

Decision importante: el diseno inicial evaluo LlamaIndex, pero la implementacion final y entregable usan un pipeline propio. La documentacion final fue alineada a esa realidad para evitar contradicciones entre arquitectura y codigo.

## 6. APIs

### Endpoints implementados
- `GET /v1/health`
- `POST /v1/ingest`
- `POST /v1/query`

### Seguridad de API
- `X-API-Key` obligatoria en `/v1/ingest` y `/v1/query`
- `GET /v1/health` sin autenticacion para monitoreo

### Especificacion
- archivo OpenAPI: `docs/api/openapi.yaml`

## 7. Seguridad

### Amenazas principales
- prompt injection
- data leakage
- acceso no autorizado
- abuso de costo y denegacion de servicio
- ingesta maliciosa de archivos
- hallucinations por contexto insuficiente

### Controles actuales
- API key
- rate limiting
- validacion de archivos
- secretos fuera del repo
- respuesta acotada al contexto
- `trace_id` por request

### Evidencia
- `reports/security_scan.json`
- `bandit=ok`
- `pip-audit=ok`
- `gitleaks=ok`

### Riesgos residuales
- rate limiting en memoria
- sin WAF
- sin moderacion avanzada del corpus

## 8. Implementacion

### Flujo de ingesta
1. Validacion de archivo
2. Parseo documental
3. Chunking
4. Generacion de embeddings
5. Upsert en `documents_chunks`

### Parametros RAG implementados
- `chunk_size = 800`
- `chunk_overlap = 100`
- `top_k = 5`
- `similarity_threshold = 0.75`
- `embedding_model = text-embedding-3-large`
- `embedding_dimensions = 3072`

### Justificacion tecnica
- `chunk_size = 800`: permite conservar contexto suficiente sin enviar fragmentos excesivamente grandes al retrieval.
- `chunk_overlap = 100`: reduce perdida de continuidad entre fragmentos contiguos.
- `top_k = 5`: equilibrio razonable entre cobertura contextual y costo de inferencia.
- `similarity_threshold = 0.75`: evita usar contexto debil o poco relacionado.
- `text-embedding-3-large`: mejora calidad semantica del retrieval para documentacion funcional y tecnica.
- `3072 dimensiones`: mayor riqueza semantica, aceptable para el alcance del MVP.

### Flujo de consulta
1. Embedding de la consulta
2. Retrieval vectorial en PostgreSQL + pgvector
3. Seleccion de hasta `top_k = 5` fragmentos
4. Filtro por `similarity_threshold = 0.75`
5. Construccion de contexto final
6. Generacion con LLM
7. Respuesta con fuentes, tokens y `trace_id`

### Parametros operativos relevantes
- `rate_limit_per_minute = 30`
- `request_timeout_s = 5`
- autenticacion por `X-API-Key` en `/v1/query` y `/v1/ingest`

## 9. Pruebas y validacion

### Resultado actual
- `38 tests passing`
- cobertura total `84%`

### Evidencia
- cobertura: `reports/coverage.xml`
- evaluacion RAGAS-style: `reports/ragas_report.json`
- notebook: `notebooks/evaluation.ipynb`
- dataset: `notebooks/eval_dataset.json`

### Metricas RAGAS-style actuales
- `faithfulness=0.3792`
- `answer_relevancy=0.1663`
- `context_recall=0.5`
- `context_precision=0.5`

Estas metricas son linea base de MVP, no una optimizacion final de calidad.

## 10. Rendimiento

### Operacion normal evaluada
- prueba local con `10` VUs por `60s`
- `p95=3005.60 ms`
- `error_rate=0.78%`

### Stress test
- prueba cloud con `50` VUs por `60s`
- `p95=3363.01 ms`
- `error_rate=89.40%`

Interpretacion: el stress test se documenta como limite operativo del entorno actual, no como comportamiento normal esperado del sistema.

## 11. Costos

### Entorno
- Cloud Run
- Cloud SQL PostgreSQL 16
- Artifact Registry
- OpenAI

### Estimacion mensual
- rango aproximado: `31 a 71 USD/mes`
- principal driver: Cloud SQL si permanece activo

### Diferencia entre estimacion y realidad
La estimacion inicial (`65 USD/mes`) sigue siendo razonable para servicio activo continuo. La validacion observada fue mas barata porque el uso fue esporadico y la instancia SQL aparecio en estado `STOPPED`.

## 12. Observabilidad
- `trace_id` por request y header `X-Trace-Id`
- logging de metodo, path, estado y latencia
- endpoint `/v1/health`
- reportes en `reports/`

## 13. Despliegue

### CI/CD
- CI: `.github/workflows/ci.yml`
- Deploy: `.github/workflows/deploy.yml`

### Servicio actual
- nombre: `odoo-knowledge-copilot`
- revision observada: `odoo-knowledge-copilot-00003-76c`
- URL: `https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app`

### Validacion final
```bash
curl -fsS https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app/v1/health
```

## 14. Conclusiones
- El objetivo funcional del MVP se cumple.
- La arquitectura es defendible y reproducible.
- La implementacion ya cubre API, RAG, seguridad minima, pruebas, reportes y despliegue cloud.
- Los limites actuales estan en calidad de retrieval y escalabilidad bajo alta concurrencia.

## 15. Lecciones aprendidas
- Para sustentacion final importa mas la coherencia entre codigo y documentacion que una arquitectura “bonita” no implementada.
- Un pipeline propio bien acotado fue suficiente para el alcance real.
- Las metricas deben presentarse separando operacion normal de stress test para no sobre-vender el sistema.

## 16. Roadmap
- mejorar retrieval y curacion del corpus
- introducir rate limiting distribuido
- evaluar cache para reducir costo y latencia
- ampliar observabilidad y dashboards
- reevaluar framework RAG si aparecen agentes o tool calling complejo

## 17. Referencias
- `docs/entregable_01/entregable_01.md`
- `docs/entregable-02/arquitectura.md`
- `docs/entregable-02/amenazas-stride.md`
- `docs/entregable-02/system-prompt.md`
- `docs/final/stack-decision.md`
- `docs/final/implementation.md`
- `docs/final/testing.md`
- `docs/final/deployment.md`
- `docs/final/security.md`
- `docs/final/costs.md`
- `docs/final/results.md`
