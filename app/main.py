from fastapi import FastAPI

app = FastAPI(title="Odoo Knowledge Copilot")


@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok", "service": "odoo-knowledge-copilot"}
