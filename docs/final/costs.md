# Costos

## Entorno usado
El entorno validado combina:
- Cloud Run para la API
- Cloud SQL PostgreSQL 16 para persistencia vectorial
- Artifact Registry para la imagen Docker
- OpenAI para embeddings y generación

Observación real del entorno al `2026-04-23`:
- servicio Cloud Run: `odoo-knowledge-copilot`
- repositorio Artifact Registry: `odoo-copilot`
- instancia Cloud SQL: `odoo-kc-pg`
- estado observado de Cloud SQL: `STOPPED`

## Costo real observado en la validacion
No se cerró una factura mensual consolidada dentro del repo, por lo que **no existe evidencia de costo real exacto**. Lo que sí puede afirmarse con base en la configuración observada es:
- durante la validación académica, el costo variable estuvo dominado por llamadas a OpenAI y por despliegues puntuales;
- el mayor costo fijo potencial del stack no viene de Cloud Run, sino de Cloud SQL si la instancia permanece encendida de forma continua;
- al estar `odoo-kc-pg` en estado `STOPPED` al momento de revisión, el costo operativo observado para pruebas esporádicas fue menor que la estimación mensual inicial.

## Estimacion mensual operativa

| Componente | Rango mensual estimado | Comentario |
|---|---:|---|
| Cloud Run | 0 a 10 USD | Bajo tráfico y escalado por demanda |
| Cloud SQL | 25 a 40 USD | Principal costo fijo si la instancia queda activa |
| Artifact Registry | menor a 1 USD | Costo marginal por imagen y almacenamiento |
| OpenAI | 5 a 15 USD | Depende del volumen de queries, embeddings e iteraciones |
| Logs y red | 1 a 5 USD | Marginal para el tamaño actual |

**Costo mensual aproximado del entorno activo:** `31 a 71 USD/mes`

## Servicio que genera mayor costo
El servicio con mayor peso económico esperado es **Cloud SQL**, porque introduce un costo base más estable que Cloud Run en un MVP de bajo tráfico.

## Diferencia entre estimacion y realidad
- Estimación inicial del entregable 1: `65 USD/mes`.
- Lectura actual: la estimación sigue siendo defendible como escenario de servicio activo permanente.
- Realidad observada en validación: menor a esa cifra, porque el uso fue esporádico y la instancia SQL no estaba activa al momento de revisión.

## Palancas de optimizacion
1. Apagar o reducir Cloud SQL fuera de ventanas de evaluación.
2. Reducir tokens por consulta ajustando `top_k`, chunk size y longitud de contexto.
3. Cachear respuestas frecuentes o embeddings ya calculados para bajar llamadas repetidas a OpenAI.
