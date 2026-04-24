# ADR-002 — Seleccion del Vector Store

## Estado
Aceptado

## Contexto
El sistema necesita almacenar embeddings y metadatos documentales con bajo costo operativo, despliegue reproducible y una integracion directa con el backend Python actual.

## Decision
Se adopta **PostgreSQL con pgvector** como vector store para la version 1.0 del sistema.

## Alternativas evaluadas

| Alternativa | Costo operativo | Simplicidad de despliegue | Escalabilidad esperada | Control de datos | Integracion actual |
|---|---:|---:|---:|---:|---:|
| PostgreSQL + pgvector | 5/5 | 5/5 | 3/5 | 5/5 | 5/5 |
| Pinecone | 2/5 | 4/5 | 5/5 | 3/5 | 3/5 |
| Qdrant | 4/5 | 3/5 | 4/5 | 4/5 | 3/5 |
| Weaviate | 3/5 | 2/5 | 4/5 | 4/5 | 2/5 |

## Justificacion
- El proyecto ya usa PostgreSQL y `pgvector` de forma explicita en [`app/services/vector_service.py`](../../app/services/vector_service.py).
- Permite mantener un stack corto y entendible para un MVP.
- Evita sumar otro servicio administrado solo para retrieval vectorial.

## Trade-offs

### Positivos
- Menor costo y menor dispersión operativa.
- Integracion natural con SQL, metadatos y persistencia existente.
- Facilita reproducibilidad local con Docker Compose.

### Negativos
- Escala peor que un vector DB dedicado si el corpus o la concurrencia crecen mucho.
- Puede requerir tuning adicional si aumentan embeddings, filtros y volumen de consultas.

## Alternativas descartadas
- **Pinecone**: muy comodo para escalar, pero agrega dependencia externa y costo fijo/variable mayor para este alcance.
- **Qdrant**: buena opcion intermedia, pero implicaba sumar otro servicio sin una necesidad inmediata.
- **Weaviate**: potente, pero excesivo para el tamaño actual del corpus y del MVP.

## Consecuencias
- Se privilegia simplicidad y costo sobre especializacion extrema.
- El retrieval queda fuertemente acoplado a PostgreSQL, aunque la abstraccion `VectorService` reduce el esfuerzo de migracion.

## Condicion de revision medible
Revisar esta decision si ocurre cualquiera de estas condiciones:
- El corpus supera `100,000` chunks indexados.
- El `p95` de retrieval supera `500 ms` en operacion normal.
- Se requiere multi-tenant fuerte o aislamiento avanzado por cliente.
- Se necesitan capacidades nativas de re-ranking o filtrado vectorial no cubiertas por el stack actual.
