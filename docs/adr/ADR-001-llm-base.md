# ADR-001 — Selección del Modelo LLM Base

## Estado
Aceptado

## Contexto

El sistema debe responder consultas funcionales y técnicas sobre documentación Odoo en español, manteniendo un costo razonable, una latencia aceptable y una integración simple para el MVP.

## Decisión

Se adopta **GPT-4o-mini** como modelo LLM base para la versión 1.0 del sistema.

## Alternativas evaluadas

- GPT-4o-mini
- Claude 3.5 Sonnet
- Gemini 1.5 Pro
- Llama 3 self-hosted

## Justificación

GPT-4o-mini ofrece:

- buena calidad de respuesta,
- latencia adecuada para demo,
- integración madura con Python,
- costo más controlado que opciones más pesadas,
- menor complejidad operativa que un modelo self-hosted.

## Consecuencias

### Positivas
- implementación rápida,
- buena DX,
- menor esfuerzo de operación,
- adecuado para MVP.

### Negativas
- dependencia de proveedor externo,
- costo por consumo,
- menor control que un modelo self-hosted.

## Revisión futura

Revisar esta decisión si:

- el costo mensual crece demasiado,
- la latencia p95 no cumple,
- se necesita operación on-premise,
- un modelo open source alcanza calidad comparable con menor TCO.