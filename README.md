# Odoo Knowledge Copilot

Asistente AI/LLM con arquitectura RAG orientado a soporte funcional y técnico sobre Odoo.

## Descripción

Odoo Knowledge Copilot permite consultar documentación funcional, técnica y operativa de Odoo usando lenguaje natural. La solución utiliza un pipeline RAG para recuperar fragmentos relevantes desde un repositorio documental y generar respuestas fundamentadas con apoyo de un LLM.

## Objetivo del proyecto

Diseñar e implementar un MVP que permita:

- ingerir documentos técnicos y funcionales,
- indexarlos semánticamente,
- responder preguntas en lenguaje natural,
- devolver referencias a las fuentes consultadas,
- mantener trazabilidad, seguridad básica y arquitectura desplegable en contenedores.

## Caso de uso principal

Usuarios internos del ecosistema Odoo, como:

- consultores funcionales,
- desarrolladores,
- soporte,
- personal en onboarding técnico.

Ejemplo de consulta:

> ¿Cómo se configura la aprobación de órdenes de compra en Odoo 18?

## Arquitectura base

La solución está compuesta por:

- FastAPI como capa de exposición de APIs,
- LlamaIndex como orquestador del pipeline RAG,
- PostgreSQL + pgvector como vector store,
- OpenAI GPT-4o-mini como modelo base,
- Redis opcional para rate limiting y caché,
- Docker Compose para despliegue MVP.

## Estructura documental

- `docs/entregable-02/arquitectura.md`: documento principal del entregable 2
- `docs/adr/`: decisiones arquitectónicas
- `docs/api/openapi.yaml`: especificación inicial de la API
- `docs/entregable-02/*.mmd`: diagramas Mermaid
- `docs/entregable-02/system-prompt.md`: prompt base del sistema
- `docs/entregable-02/amenazas-stride.md`: modelo de amenazas

## Alcance del MVP

Incluye:

- API REST,
- ingesta de documentos PDF/Markdown,
- chunking,
- embeddings,
- indexación vectorial,
- retrieval semántico,
- generación de respuestas con fuentes,
- autenticación básica por API key,
- trazabilidad mínima.

No incluye en esta fase:

- UI web final,
- fine-tuning,
- multi-tenant avanzado,
- IAM enterprise,
- despliegue Kubernetes.

## Stack tecnológico

- Python
- FastAPI
- LlamaIndex
- PostgreSQL
- pgvector
- OpenAI API
- Docker Compose
- Redis (opcional)

## Entregable 2

Este repositorio contiene el segundo entregable del capítulo 2 del proyecto, centrado en el diseño arquitectónico del sistema.

## Navegación rápida

- [Arquitectura](docs/entregable-02/arquitectura.md)
- [ADR-001](docs/adr/ADR-001-llm-base.md)
- [ADR-002](docs/adr/ADR-002-vector-store.md)
- [ADR-003](docs/adr/ADR-003-rag-orchestration.md)
- [OpenAPI](docs/api/openapi.yaml)
- [System Prompt](docs/entregable-02/system-prompt.md)
- [Amenazas STRIDE](docs/entregable-02/amenazas-stride.md)

## Autor

Hector Fidel Cruz Rodriguez