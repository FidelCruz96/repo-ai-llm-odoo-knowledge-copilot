from typing import Any

from pydantic import BaseModel, Field


class SourceItem(BaseModel):
    doc_id: str
    doc_name: str
    page: int | None = None
    score: float


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=8000)
    session_id: str | None = None
    filters: dict[str, Any] | None = None
    stream: bool = False


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    tokens_used: int | None = None
    latency_ms: float
    trace_id: str


class IngestedDocument(BaseModel):
    file: str
    chunks: int
    status: str


class IngestResponse(BaseModel):
    ingested: list[IngestedDocument]


class HealthResponse(BaseModel):
    status: str
    version: str
    checks: dict[str, str]
