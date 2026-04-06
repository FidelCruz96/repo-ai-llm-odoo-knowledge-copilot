# Modelo de Amenazas — STRIDE

## Resumen

Se aplicó STRIDE para identificar amenazas principales en la arquitectura del MVP.

| Categoría | Amenaza | Impacto | Control propuesto | Riesgo |
|---|---|---|---|---|
| Spoofing | Uso no autorizado de la API | Acceso indebido | API keys, rotación, HTTPS | Alto |
| Tampering | Prompt injection o contaminación documental | Respuestas manipuladas | guardrails, validación, curación del corpus | Crítico |
| Repudiation | Negación de acciones realizadas | Falta de trazabilidad | logs con request_id y trace_id | Medio |
| Information Disclosure | Exposición de información sensible | Riesgo reputacional y técnico | filtrado, control documental, revisión de outputs | Crítico |
| Denial of Service | Saturación de consultas o abuso | Caída de servicio o sobrecosto | rate limiting, cuotas, timeouts | Alto |
| Elevation of Privilege | Forzar comportamientos fuera del alcance | Uso indebido del sistema | diseño read-only y validaciones estrictas | Alto |

## Top 3 amenazas críticas

### 1. Prompt Injection
Intentos de alterar el comportamiento del modelo o hacer que ignore instrucciones de grounding.

### 2. Data Leakage
Riesgo de exposición de información interna o sensible a través de las respuestas.

### 3. DoS / Sobrecosto
Consultas masivas o maliciosas que degradan el servicio o elevan el costo del proveedor LLM.