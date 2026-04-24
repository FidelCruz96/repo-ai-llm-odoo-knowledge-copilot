from __future__ import annotations

from dataclasses import dataclass

from app.core.config import Settings
from app.models.db_models import EmbeddedChunkRecord
from app.models.schemas import QueryRequest
from app.services.ingest_service import IngestService
from app.services.rag_service import RagService


def _build_settings() -> Settings:
    return Settings(
        APP_NAME="odoo-knowledge-copilot",
        APP_ENV="test",
        APP_VERSION="0.1.0",
        API_KEY="test",
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        REDIS_URL="redis://localhost:6379/0",
        MODEL_NAME="gpt-4o-mini",
        EMBEDDING_MODEL="text-embedding-3-large",
        OPENAI_API_KEY="test-key",
        TOP_K=5,
        SIMILARITY_THRESHOLD=0.2,
        CHUNK_SIZE=120,
        CHUNK_OVERLAP=20,
        EMBEDDING_DIMENSIONS=3,
        REQUEST_TIMEOUT_S=2,
    )


class FakeEmbeddingService:
    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    @staticmethod
    def _embed(text: str) -> list[float]:
        size = float(max(len(text), 1))
        alpha = float(sum(1 for c in text.lower() if c.isalpha()))
        digits = float(sum(1 for c in text if c.isdigit()))
        return [alpha / size, digits / size, min(size / 1000.0, 1.0)]


@dataclass
class InMemoryVectorService:
    chunks: list[EmbeddedChunkRecord]

    def upsert_chunks(self, chunks: list[EmbeddedChunkRecord]) -> None:
        self.chunks.extend(chunks)

    def search(self, query_embedding: list[float], top_k: int, filters: dict | None = None) -> list[dict]:
        rows = []
        for chunk in self.chunks:
            if filters and filters.get("module") and chunk.module != filters["module"]:
                continue
            score = _score(query_embedding, chunk.embedding)
            rows.append(
                {
                    "id": chunk.id,
                    "doc_id": chunk.doc_id,
                    "doc_name": chunk.doc_name,
                    "source_type": chunk.source_type,
                    "page": chunk.page,
                    "module": chunk.module,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "score": score,
                }
            )
        rows.sort(key=lambda item: item["score"], reverse=True)
        return rows[:top_k]


class FakeLLMService:
    def generate_answer(self, query: str, context_chunks: list[dict]):
        class Result:
            answer = "En Odoo, el picking representa una operación logística."
            tokens_used = 88
            model = "fake-llm"
            finish_reason = "stop"

        return Result()


def _score(query_embedding: list[float], chunk_embedding: list[float]) -> float:
    distance = sum(abs(a - b) for a, b in zip(query_embedding, chunk_embedding, strict=True))
    return max(0.0, 1.0 - distance)


def test_rag_pipeline_end_to_end_with_in_memory_store() -> None:
    settings = _build_settings()
    embedding_service = FakeEmbeddingService()
    vector_service = InMemoryVectorService(chunks=[])
    llm_service = FakeLLMService()

    ingest_service = IngestService(
        settings=settings,
        embedding_service=embedding_service,
        vector_service=vector_service,  # type: ignore[arg-type]
    )
    rag_service = RagService(
        settings=settings,
        embedding_service=embedding_service,  # type: ignore[arg-type]
        vector_service=vector_service,  # type: ignore[arg-type]
        llm_service=llm_service,  # type: ignore[arg-type]
    )

    ingest_result = ingest_service.ingest_files(
        files=[
            (
                "inventario_odoo.md",
                b"# Inventario\nUn picking representa la operacion de movimiento de stock en Odoo.",
            )
        ],
        module="inventory",
    )
    assert ingest_result.ingested[0].status == "ok"
    assert ingest_result.ingested[0].chunks >= 1

    response = rag_service.answer_query(
        QueryRequest(
            query="Que es un picking en Odoo?",
            filters={"module": "inventory"},
        )
    )

    assert response.answer != ""
    assert len(response.sources) >= 1
    assert response.sources[0].score >= settings.similarity_threshold
    assert response.trace_id != ""
    assert response.latency_ms >= 0
