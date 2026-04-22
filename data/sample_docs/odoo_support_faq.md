# Odoo Support FAQ

La API expone `/v1/health`, `/v1/ingest` y `/v1/query`.
Formatos soportados para ingesta: PDF, MD, Markdown y TXT.
Si no hay contexto suficiente para una respuesta confiable, el sistema debe indicarlo explícitamente.
Los metadatos por chunk incluyen `doc_id`, `doc_name`, `page`, `module` y `chunk_index`.
