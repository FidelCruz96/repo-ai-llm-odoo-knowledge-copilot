# ADR-001 — Seleccion del Modelo LLM Base

## Estado
Aceptado

## Contexto
El sistema debe responder consultas funcionales y tecnicas sobre documentacion Odoo en espanol con costo razonable, baja latencia y una integracion simple para un MVP desplegado en Cloud Run.

## Decision
Se adopta **OpenAI `gpt-4o-mini`** como modelo LLM base para la version 1.0 del sistema.

## Alternativas evaluadas

| Alternativa | Calidad esperada | Latencia esperada | Complejidad operativa | Costo relativo | Integracion actual |
|---|---:|---:|---:|---:|---:|
| OpenAI `gpt-4o-mini` | 4/5 | 4/5 | 5/5 | 4/5 | 5/5 |
| Claude | 4/5 | 4/5 | 4/5 | 3/5 | 3/5 |
| Gemini | 4/5 | 4/5 | 4/5 | 3/5 | 3/5 |
| Llama self-hosted | 3/5 | 2/5 | 1/5 | 2/5 | 2/5 |

## Justificacion
- El codigo actual ya esta integrado contra la API de OpenAI en [`app/services/llm_service.py`](../../app/services/llm_service.py) y usa `gpt-4o-mini` por configuracion.
- Entrega una relacion conveniente entre costo, velocidad e implementacion para un MVP academico.
- Reduce tiempo de integracion respecto a alternativas que exigen cambios de SDK, hosting dedicado o evaluacion adicional de calidad.

## Trade-offs

### Positivos
- Integracion directa con el stack Python actual.
- Menor complejidad de operacion que un modelo self-hosted.
- Latencia razonable para la meta funcional del MVP.

### Negativos
- Dependencia de un proveedor externo.
- Costo variable por consumo de tokens.
- Menor control de infraestructura que en una opcion self-hosted.

## Alternativas descartadas
- **Claude**: buena calidad, pero implicaba cambiar proveedor y adaptar integracion sin evidencia suficiente de mejora proporcional para este MVP.
- **Gemini**: opcion valida, pero no era la ruta mas corta para cerrar el entregable con menor riesgo.
- **Llama self-hosted**: aporta control, pero sube mucho el costo operativo y la complejidad de despliegue para esta fase.

## Consecuencias
- La solucion queda optimizada para entrega rapida y validacion funcional.
- La arquitectura conserva un punto de cambio claro en `LLMService`, por lo que una sustitucion futura sigue siendo viable.

## Condicion de revision medible
Revisar esta decision si ocurre cualquiera de estas condiciones:
- `latency_p95_ms` de operacion normal supera `3000 ms` de forma sostenida.
- El costo mensual de inferencia supera el `40%` del costo total operativo.
- Se requiere despliegue on-premise o sin dependencia de proveedor externo.
- Una alternativa alcanza calidad equivalente con integracion estimada menor a `2 dias` de trabajo.
