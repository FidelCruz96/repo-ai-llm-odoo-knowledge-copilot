from fastapi import FastAPI

app = FastAPI(
    title="Odoo Knowledge Copilot",
    version="1.0.0",
    description="API MVP para consultas RAG sobre documentación funcional y técnica de Odoo"
)


@app.get("/")
def root() -> dict:
    return {
        "name": "Odoo Knowledge Copilot",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/v1/health")
def health() -> dict:
    return {"status": "ok", "service": "odoo-knowledge-copilot"}