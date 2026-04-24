# ADR-003 — Orquestacion del Pipeline RAG

## Estado
Aceptado

## Contexto
El proyecto requiere un pipeline RAG claro para ingestión, embeddings, retrieval y generación. La decisión final debe reflejar la implementación real del repositorio y no solo el diseño inicial.

## Decision
Se adopta un **pipeline RAG propio en Python**, compuesto por servicios separados para `ingest`, `embedding`, `vector`, `rag` y `llm`.

## Alternativas evaluadas

| Alternativa | Velocidad de implementacion | Alineacion con el codigo real | Flexibilidad futura | Complejidad accidental | Dependencia externa |
|---|---:|---:|---:|---:|---:|
| Pipeline propio | 4/5 | 5/5 | 4/5 | 4/5 | 5/5 |
| LlamaIndex | 4/5 | 1/5 | 3/5 | 3/5 | 2/5 |
| LangChain | 3/5 | 1/5 | 4/5 | 2/5 | 2/5 |

## Justificacion
- La implementacion actual ya existe como pipeline propio en [`app/services/rag_service.py`](../../app/services/rag_service.py), [`app/services/ingest_service.py`](../../app/services/ingest_service.py), [`app/services/vector_service.py`](../../app/services/vector_service.py), [`app/services/embedding_service.py`](../../app/services/embedding_service.py) y [`app/services/llm_service.py`](../../app/services/llm_service.py).
- No hay dependencias activas de LlamaIndex ni LangChain en `requirements.txt`.
- Documentar LlamaIndex como decision final generaba una inconsistencia objetiva con el codigo entregado.

## Trade-offs

### Positivos
- Control total del flujo y de los contratos internos.
- Menos capas de abstraccion y menor riesgo de “framework drift”.
- Facilita explicar el pipeline real durante la sustentacion.

### Negativos
- Hay mas codigo propio que mantener.
- Algunas utilidades de frameworks maduros deben resolverse manualmente.

## Alternativas descartadas
- **LlamaIndex**: fue una opcion razonable en la fase de diseno, pero no corresponde a la implementacion final.
- **LangChain**: aporta flexibilidad para agentes y tools, pero agrega complejidad no necesaria para el alcance actual.

## Consecuencias
- La documentacion final queda alineada con el repositorio real.
- El sistema conserva margen de evolucion: si el proyecto pasa a agentes, tool calling complejo o varios retrievers, se puede reevaluar.

## Condicion de revision medible
Revisar esta decision si ocurre cualquiera de estas condiciones:
- Se necesitan `2` o mas pipelines RAG con comportamiento diferente.
- Se agregan agentes/tool-calling multi-step al producto.
- El tiempo de mantenimiento del pipeline propio supera `1 sprint` por semestre solo en plumbing.
- Se detecta que una libreria externa reduce al menos `30%` del codigo orquestador sin degradar observabilidad ni control.
