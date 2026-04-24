# Testing

## Estrategia

La validación del sistema se diseñó en tres niveles complementarios:

1. **Unit tests**
   - orientados a utilidades, validaciones y servicios críticos;
   - permiten verificar lógica aislada y reducir regresiones.

2. **Test de integración**
   - enfocado en el pipeline RAG de extremo a extremo en entorno controlado;
   - valida que la secuencia ingesta → retrieval → generación responda según el contrato esperado.

3. **Pruebas de rendimiento**
   - realizadas con `k6`;
   - separadas en:
     - una **prueba base del MVP** para validar comportamiento bajo carga moderada;
     - una **prueba de estrés** para identificar límites operativos del entorno actual.

La cobertura automatizada se mide con `pytest-cov`.

## Comandos ejecutados

- `make test`
- `make coverage`

## Estado actual

- Suite automatizada: **38 tests passing**
- Cobertura total: **84%** (`reports/coverage.xml`)

## Evidencia ejecutada

### Validación funcional en cloud
La API pública fue validada en Cloud Run:

- `GET /v1/health` → `healthy`
- `POST /v1/ingest` → `200`
- `POST /v1/query` → `200`

### Evaluación RAGAS-style
- Reporte generado en: `reports/ragas_report.json`

### Pruebas de carga
- Prueba base MVP ejecutada con `10` VUs (`60s`) y guardada en:
  - `reports/load_test_report_10vus_local.json`
- Prueba de estrés ejecutada con `50` VUs (`60s`) y guardada en:
  - `reports/load_test_report_50vus.json`

## Resultado de carga

### 1. Prueba base del MVP
Condiciones:
- `10` VUs
- `60s`
- entorno local

Resultados:
- `error_rate=0.78%`
- `p50=1726.88 ms`
- `p95=3005.60 ms`
- `p99=3312.68 ms`
- `throughput=4.09 req/s`

Interpretación:
- Esta prueba se utiliza como referencia funcional del MVP bajo carga moderada.
- El sistema mantiene una tasa de error baja.
- La latencia `p95` queda apenas por encima del umbral objetivo de `3000 ms`, por lo que el comportamiento se considera aceptable para una primera versión, aunque todavía con margen de optimización.

### 2. Prueba de estrés / límite operativo
Condiciones:
- `50` VUs
- `60s`
- entorno Cloud Run

Resultados:
- `error_rate=89.40%`
- `p50=205.97 ms`
- `p95=3363.01 ms`
- `p99=4085.16 ms`
- `throughput=47.45 req/s`

Interpretación:
- Esta prueba debe interpretarse como **stress test**, no como benchmark objetivo de operación normal del MVP.
- Bajo esta concurrencia, el sistema no cumple los objetivos de estabilidad ni latencia.
- La mediana global (`p50`) queda sesgada por respuestas fallidas rápidas, por lo que su lectura aislada no representa adecuadamente la experiencia real de respuestas exitosas.
- Durante la validación en Cloud Run se observó estado `degraded` con `vector_store=error` en `/v1/health`, lo que indica que el resultado refleja un límite operativo del entorno evaluado.

## Conclusiones de testing

1. El sistema **sí supera correctamente las validaciones funcionales principales**:
   - endpoints operativos,
   - pipeline RAG end-to-end,
   - respuesta con fuentes,
   - trazabilidad básica.

2. La cobertura automatizada (**84%**) y la suite de **38 tests** dan una base sólida de calidad para esta fase del proyecto.

3. La prueba base de `10` VUs confirma que el MVP puede operar de forma funcional bajo carga moderada, aunque todavía requiere optimización fina para cumplir con mayor holgura el umbral de latencia.

4. La prueba de `50` VUs evidencia el límite actual del entorno bajo estrés alto y aporta información útil para priorizar mejoras de escalabilidad.
