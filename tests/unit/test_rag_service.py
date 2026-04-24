from app.core.config import Settings
from app.models.schemas import QueryRequest
from app.services.rag_service import RagService


class FakeEmbeddingService:
    def embed_query(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class FakeVectorService:
    def __init__(self, chunks: list[dict]) -> None:
        self._chunks = chunks

    def search(self, query_embedding: list[float], top_k: int, filters: dict | None = None) -> list[dict]:
        return self._chunks[:top_k]


class FakeLLMService:
    def generate_answer(self, query: str, context_chunks: list[dict]):
        class Result:
            answer = "Respuesta basada en contexto"
            tokens_used = 123
            model = "fake-model"
            finish_reason = "stop"

        return Result()


def build_settings(similarity_threshold: float = 0.75, top_k: int = 5) -> Settings:
    return Settings(
        APP_NAME="odoo-knowledge-copilot",
        APP_ENV="test",
        APP_VERSION="0.1.0",
        API_KEY="test",
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        REDIS_URL="redis://localhost:6379/0",
        MODEL_NAME="gpt-4o-mini",
        EMBEDDING_MODEL="text-embedding-3-large",
        OPENAI_API_KEY="test",
        TOP_K=top_k,
        SIMILARITY_THRESHOLD=similarity_threshold,
        CHUNK_SIZE=800,
        CHUNK_OVERLAP=100,
        EMBEDDING_DIMENSIONS=3072,
        REQUEST_TIMEOUT_S=2,
    )


def test_answer_query_returns_answer_and_sources() -> None:
    chunks = [
        {"doc_id": "doc-1", "doc_name": "manual.pdf", "page": 3, "score": 0.91, "content": "Texto A"},
        {"doc_id": "doc-2", "doc_name": "guide.md", "page": 2, "score": 0.83, "content": "Texto B"},
    ]
    service = RagService(
        settings=build_settings(similarity_threshold=0.8, top_k=2),
        embedding_service=FakeEmbeddingService(),
        vector_service=FakeVectorService(chunks=chunks),
        llm_service=FakeLLMService(),
    )

    response = service.answer_query(QueryRequest(query="Como configuro compras en Odoo?"))

    assert response.answer == "Respuesta basada en contexto"
    assert response.tokens_used == 123
    assert len(response.sources) == 2
    assert response.sources[0].doc_id == "doc-1"
    assert response.latency_ms >= 0
    assert response.trace_id


def test_answer_query_without_context_returns_fallback() -> None:
    chunks = [
        {"doc_id": "doc-1", "doc_name": "manual.pdf", "page": 3, "score": 0.3, "content": "Texto A"},
    ]
    service = RagService(
        settings=build_settings(similarity_threshold=0.8),
        embedding_service=FakeEmbeddingService(),
        vector_service=FakeVectorService(chunks=chunks),
        llm_service=FakeLLMService(),
    )

    response = service.answer_query(QueryRequest(query="Pregunta sin contexto"))

    assert response.answer == "No encontré suficiente contexto para responder con precisión."
    assert response.tokens_used is None
    assert response.sources == []
