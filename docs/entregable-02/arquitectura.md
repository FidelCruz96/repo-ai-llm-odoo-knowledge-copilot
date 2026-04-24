# Entregable 2 — Diseño de Arquitectura

## Proyecto
**Odoo Knowledge Copilot**

## Autor
Hector Fidel Cruz Rodriguez

## Fecha
2026-03-24

---

## 1. Resumen Ejecutivo

Odoo Knowledge Copilot es una solución AI/LLM con arquitectura RAG orientada a centralizar y consultar conocimiento funcional, técnico y operativo de Odoo mediante lenguaje natural. El sistema permite ingerir documentación curada, indexarla semánticamente y responder preguntas con referencias a las fuentes utilizadas.

Este entregable documenta el diseño de arquitectura del sistema, sus principales decisiones tecnológicas, el modelo de interacción, el pipeline RAG, la seguridad inicial y las amenazas más relevantes.

---

## 2. Criterios de Selección Tecnológica

Las tecnologías fueron evaluadas según:

- rendimiento,
- costo,
- ecosistema,
- madurez,
- seguridad,
- developer experience.

### Selección principal

| Capa | Tecnología elegida | Justificación |
|---|---|---|
| Backend API | FastAPI | Alto rendimiento, tipado claro, OpenAPI automático |
| Lenguaje principal | Python | Ecosistema ideal para AI/LLM y RAG |
| Orquestación RAG | LlamaIndex | Buen encaje para ingestión documental y retrieval |
| LLM base | GPT-4o-mini | Balance entre costo, velocidad y calidad |
| Embeddings | text-embedding-3-small | Costo controlado y calidad suficiente para MVP |
| Vector Store | PostgreSQL + pgvector | Bajo costo operativo y gran integración |
| Caché / rate limit | Redis (opcional) | Extensión práctica para MVP y siguientes iteraciones |
| Despliegue | Docker Compose | Simplicidad y reproducibilidad |
| Autenticación | API key | Adecuada para el alcance del MVP |

---

## 3. Arquitectura General

La solución sigue una arquitectura desacoplada basada en API, con separación entre exposición, orquestación, almacenamiento vectorial y proveedor LLM.

### Componentes principales

- Cliente consumidor de la API
- API REST con FastAPI
- Middleware de seguridad
- Servicio RAG
- Servicio de ingesta documental
- PostgreSQL con pgvector
- Repositorio documental
- Proveedor LLM externo

### 3.1 Diagrama C4 - Contexto

Ver archivo `c4-contexto.mmd` y su exportación `.png`.

### 3.2 Diagrama C4 - Contenedores

Ver archivo `c4-contenedores.mmd` y su exportación `.png`.

---

## 4. Flujo principal

1. El usuario envía una consulta en lenguaje natural.
2. La API valida credenciales y límites.
3. El servicio RAG convierte la consulta en embedding.
4. Se recuperan fragmentos relevantes desde pgvector.
5. Se construye el prompt final con contexto recuperado.
6. El LLM genera la respuesta.
7. El sistema devuelve respuesta con fuentes y trazabilidad.

### 4.1 Diagrama de secuencia request → response

Ver archivo `secuencia-query.mmd` y su exportación `.png`.

---

## 5. Pipeline RAG

### Etapas

- Ingesta documental
- Parsing
- Chunking
- Embeddings
- Indexación
- Retrieval
- Re-ranking ligero
- Generación

### Parámetros propuestos

| Parámetro | Valor |
|---|---|
| Chunk size | 700 tokens |
| Overlap | 100 tokens |
| top-k | 5 |
| Similarity threshold | 0.78 |
| Embedding model | text-embedding-3-small |
| Re-ranking | Sí, ligero |

### Justificación

Estos parámetros equilibran precisión, costo y tamaño del prompt para un MVP académico/técnico con documentación estructurada de Odoo.

### 5.1 Decisiones de diseño del pipeline

- Se usa chunking recursivo para conservar coherencia semántica.
- Se usa top-k=5 para limitar inflación del prompt.
- Se propone threshold de 0.78 para reducir ruido.
- Se contempla re-ranking ligero para mejorar precisión final.

---

## 6. Seguridad Inicial

### Medidas consideradas

- API key en header `X-API-Key`
- HTTPS
- rate limiting
- validación de payloads
- secretos por variables de entorno
- logs estructurados sin exponer credenciales
- control del corpus documental

---

## 7. Observabilidad

Se propone registrar:

- request_id
- trace_id
- latencia
- tokens consumidos
- costo estimado
- errores
- estado del retrieval
- fuentes usadas

---

## 8. Decisiones Arquitectónicas

Las decisiones principales se documentan en:

- `docs/adr/ADR-001-llm-base.md`
- `docs/adr/ADR-002-vector-store.md`
- `docs/adr/ADR-003-rag-orchestration.md`

---

## 9. Riesgos principales

- prompt injection,
- filtración de información,
- denegación de servicio,
- dependencia de proveedor externo,
- crecimiento de latencia conforme crezca el corpus.

---

## 10. Comparación con el agente actual basado en tools sobre Odoo

Actualmente existe un agente que consulta Odoo directamente mediante tools y endpoints orientados a operaciones como `search`, `read`, `group` y `count`. Ese enfoque es ideal para responder sobre datos vivos del ERP, como ventas del mes, clientes con más facturación o agrupaciones por vendedor.

En cambio, Odoo Knowledge Copilot con RAG está orientado a responder sobre conocimiento documental: manuales, procedimientos, troubleshooting, configuraciones, onboarding técnico y conocimiento funcional.

| Criterio | Agente actual con tools sobre Odoo | Odoo Knowledge Copilot con RAG |
|---|---|---|
| Fuente principal | Datos vivos del ERP | Documentación curada |
| Tipo de consulta | Reporting y operación | Soporte funcional/técnico |
| Trazabilidad documental | Limitada | Alta |
| Valor para onboarding | Medio | Alto |
| Tiempo real | Sí | No necesariamente |
| Mejor uso | Qué está pasando ahora | Cómo funciona o cómo se hace |

### Conclusión de comparación

Ambos enfoques no compiten; se complementan.  
El agente tool-based resuelve mejor consultas operativas en tiempo real. El Copilot con RAG resuelve mejor preguntas de conocimiento persistente. La evolución natural del proyecto sería una arquitectura híbrida con un router que decida cuándo consultar datos vivos, cuándo consultar documentos y cuándo combinar ambos.

---

## 11. Conclusión

La arquitectura propuesta es consistente con el alcance del MVP y prioriza trazabilidad, grounding y control operativo. La combinación FastAPI + LlamaIndex + PostgreSQL/pgvector + GPT-4o-mini ofrece una base sólida para una primera versión funcional sin caer en sobrearquitectura. En pocas palabras: suficiente músculo, cero humo innecesario.