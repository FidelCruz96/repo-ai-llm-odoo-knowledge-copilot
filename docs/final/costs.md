# Costos (estimación)

## Drivers de costo
- Tokens OpenAI (embeddings + generación).
- Cloud Run (CPU/RAM por request).
- Cloud SQL (instancia + almacenamiento).
- Egreso de red y almacenamiento de documentos.

## Supuestos base MVP
- 1,000 consultas/día.
- 5–10 documentos iniciales, crecimiento bajo.
- `top_k=5`, chunking moderado.

## Recomendaciones
- Limitar contexto para reducir tokens.
- Cachear respuestas frecuentes cuando aplique.
- Ajustar autoscaling mínimo en Cloud Run para costo/latencia.
