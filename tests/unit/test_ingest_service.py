from app.core.config import Settings
from app.models.db_models import EmbeddedChunkRecord
from app.services.ingest_service import IngestService


class FakeEmbeddingService:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorService:
    def __init__(self) -> None:
        self.saved_chunks: list[EmbeddedChunkRecord] = []

    def upsert_chunks(self, chunks: list[EmbeddedChunkRecord]) -> None:
        self.saved_chunks.extend(chunks)


def test_ingest_files_returns_ok_and_upserts_chunks() -> None:
    settings = Settings(
        APP_NAME="odoo-knowledge-copilot",
        APP_ENV="test",
        APP_VERSION="0.1.0",
        API_KEY="test",
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        REDIS_URL="redis://localhost:6379/0",
        MODEL_NAME="gpt-4o-mini",
        EMBEDDING_MODEL="text-embedding-3-large",
        OPENAI_API_KEY="test",
        TOP_K=5,
        SIMILARITY_THRESHOLD=0.75,
        CHUNK_SIZE=100,
        CHUNK_OVERLAP=10,
        EMBEDDING_DIMENSIONS=3,
        REQUEST_TIMEOUT_S=2,
    )
    vector = FakeVectorService()
    service = IngestService(
        settings=settings,
        embedding_service=FakeEmbeddingService(),
        vector_service=vector,
    )

    response = service.ingest_files(
        files=[("manual.txt", b"This is a test document for Odoo ingestion." * 5)],
        module="purchase",
    )

    assert len(response.ingested) == 1
    assert response.ingested[0].status == "ok"
    assert response.ingested[0].chunks > 0
    assert len(vector.saved_chunks) == response.ingested[0].chunks
    assert all(chunk.module == "purchase" for chunk in vector.saved_chunks)
