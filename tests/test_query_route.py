from app.api.routes_query import query
from app.main import app
from app.models.schemas import QueryRequest, QueryResponse, SourceItem


class FakeRagService:
    def answer_query(self, request: QueryRequest) -> QueryResponse:
        return QueryResponse(
            answer=f"Respuesta para: {request.query}",
            sources=[
                SourceItem(doc_id="doc-1", doc_name="manual.pdf", page=1, score=0.9),
            ],
            tokens_used=200,
            latency_ms=140.5,
            trace_id="trace-123",
        )


def test_query_route_is_registered() -> None:
    paths = {route.path for route in app.routes}
    assert "/v1/query" in paths


def test_query_route_function_uses_service() -> None:
    response = query(
        request=QueryRequest(query="Que es un picking?"),
        service=FakeRagService(),
    )

    assert response.answer.startswith("Respuesta para:")
    assert response.sources[0].doc_id == "doc-1"
    assert response.trace_id == "trace-123"
