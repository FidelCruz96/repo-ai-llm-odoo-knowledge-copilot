import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import Response

from app.api.routes_health import router as health_router
from app.api.routes_ingest import router as ingest_router
from app.api.routes_query import router as query_router
from app.core.config import get_settings
from app.core.logger import configure_logging

settings = get_settings()
configure_logging()
request_logger = logging.getLogger("app.request")

app = FastAPI(
    title="Odoo Knowledge Copilot API",
    version=settings.app_version,
    description="API MVP para consultas RAG sobre documentación funcional y técnica de Odoo"
)


@app.get("/")
def root() -> dict:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs"
    }


app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(query_router)


@app.middleware("http")
async def trace_middleware(request: Request, call_next) -> Response:
    trace_id = request.headers.get("X-Trace-Id", str(uuid4()))
    started_at = perf_counter()
    response = await call_next(request)
    latency_ms = round((perf_counter() - started_at) * 1000, 2)
    response.headers["X-Trace-Id"] = trace_id
    request_logger.info(
        "request_completed method=%s path=%s status=%s latency_ms=%.2f trace_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
        trace_id,
    )
    return response
