from __future__ import annotations

import pytest

from app.core.config import Settings


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        APP_NAME="odoo-knowledge-copilot",
        APP_ENV="test",
        APP_VERSION="0.1.0",
        API_KEY="test-api-key",
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        REDIS_URL="redis://localhost:6379/0",
        MODEL_NAME="gpt-4o-mini",
        EMBEDDING_MODEL="text-embedding-3-large",
        OPENAI_API_KEY="test-openai-key",
        TOP_K=5,
        SIMILARITY_THRESHOLD=0.5,
        CHUNK_SIZE=120,
        CHUNK_OVERLAP=20,
        EMBEDDING_DIMENSIONS=3,
        REQUEST_TIMEOUT_S=2,
    )
