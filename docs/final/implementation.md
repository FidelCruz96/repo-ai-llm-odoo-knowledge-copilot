# Implementación

## Arquitectura ejecutada
- API FastAPI modular en `app/`.
- Servicios: `health`, `ingest`, `embedding`, `vector`, `llm`, `rag`.
- Utilidades: parseo documental, chunking, validación de archivos y generación de IDs.
- Seguridad básica: API Key + rate limiting por minuto.
- Trazabilidad mínima: `trace_id` en respuesta y header `X-Trace-Id`.

## Flujo de ingesta
1. Validación de archivos (tipo/tamaño).
2. Parseo (`PDF`, `MD`, `TXT`).
3. Chunking configurable.
4. Embeddings.
5. Upsert en `documents_chunks` (pgvector).

## Flujo de consulta
1. Embedding de query.
2. Retrieval vectorial con `top_k` + filtros.
3. Filtrado por `similarity_threshold`.
4. Construcción de prompt contextual.
5. Generación de respuesta con LLM.
6. Respuesta con `sources`, `tokens_used`, `latency_ms`, `trace_id`.
