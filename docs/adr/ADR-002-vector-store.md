# ADR-002 — Selección del Vector Store

## Estado
Aceptado

## Contexto

El sistema necesita almacenar embeddings y metadatos documentales con bajo costo operativo y despliegue reproducible en un MVP.

## Decisión

Se adopta **PostgreSQL con pgvector** como vector store.

## Alternativas evaluadas

- PostgreSQL + pgvector
- Qdrant
- Pinecone
- Weaviate

## Justificación

pgvector fue elegido por:

- menor costo operativo,
- integración natural con PostgreSQL,
- simplicidad de despliegue,
- capacidad suficiente para el volumen esperado del MVP.

## Consecuencias

### Positivas
- arquitectura más simple,
- menos dependencias externas,
- mejor reutilización del stack conocido,
- facilidad de mantenimiento.

### Negativas
- menor especialización que un vector DB dedicado,
- escalabilidad más limitada a gran volumen,
- puede requerir tuning adicional si el corpus crece mucho.

## Revisión futura

Revisar esta decisión si:

- aumenta significativamente el corpus,
- la latencia de retrieval empeora,
- se requiere multi-tenant fuerte,
- se necesitan capacidades avanzadas de búsqueda vectorial dedicadas.