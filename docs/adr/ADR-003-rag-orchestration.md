# ADR-003 — Selección del Framework de Orquestación RAG

## Estado
Aceptado

## Contexto

El proyecto requiere un framework que facilite ingestión, indexación, retrieval y construcción de respuestas a partir de documentación técnica y funcional.

## Decisión

Se adopta **LlamaIndex** como framework principal para el pipeline RAG.

## Alternativas evaluadas

- LlamaIndex
- LangChain
- Implementación ad hoc

## Justificación

LlamaIndex fue elegido porque:

- está más orientado a casos RAG documentales,
- simplifica la ingestión y el retrieval,
- reduce complejidad para un MVP,
- encaja bien con una arquitectura FastAPI separada.

## Consecuencias

### Positivas
- implementación más rápida,
- mejor foco en documentación,
- menor complejidad accidental.

### Negativas
- menor flexibilidad generalista que LangChain para agentes complejos,
- posible dependencia de abstracciones propias del framework.

## Revisión futura

Revisar si el proyecto evoluciona a:

- agentes multi-step,
- tool calling complejo,
- workflows con más integraciones externas.