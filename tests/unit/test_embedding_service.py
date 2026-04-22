from __future__ import annotations

import httpx
import pytest

from app.core.config import Settings
from app.services.embedding_service import EmbeddingService


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("POST", "http://test/embeddings")
            response = httpx.Response(status_code=self.status_code, request=request)
            raise httpx.HTTPStatusError("http error", request=request, response=response)

    def json(self) -> dict:
        return self._payload


def _build_settings(openai_api_key: str) -> Settings:
    return Settings(
        APP_NAME="odoo-knowledge-copilot",
        APP_ENV="test",
        APP_VERSION="0.1.0",
        API_KEY="test",
        DATABASE_URL="postgresql://test:test@localhost:5432/test",
        REDIS_URL="redis://localhost:6379/0",
        MODEL_NAME="gpt-4o-mini",
        EMBEDDING_MODEL="text-embedding-3-large",
        OPENAI_API_KEY=openai_api_key,
        TOP_K=5,
        SIMILARITY_THRESHOLD=0.75,
        CHUNK_SIZE=800,
        CHUNK_OVERLAP=100,
        EMBEDDING_DIMENSIONS=3,
        REQUEST_TIMEOUT_S=2,
    )


def test_embed_texts_returns_empty_for_empty_input() -> None:
    service = EmbeddingService(settings=_build_settings("test-key"))
    assert service.embed_texts([]) == []


def test_embed_texts_requires_openai_key() -> None:
    service = EmbeddingService(settings=_build_settings("replace_me"))
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is not configured"):
        service.embed_texts(["hola"])


def test_embed_texts_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeClient:
        def __init__(self, timeout: int) -> None:
            self.timeout = timeout

        def __enter__(self) -> "_FakeClient":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def post(self, url: str, headers: dict, json: dict) -> _FakeResponse:
            assert url.endswith("/embeddings")
            assert json["input"] == ["chunk A", "chunk B"]
            return _FakeResponse(
                status_code=200,
                payload={"data": [{"embedding": [0.1, 0.2, 0.3]}, {"embedding": [0.4, 0.5, 0.6]}]},
            )

    monkeypatch.setattr("app.services.embedding_service.httpx.Client", _FakeClient)
    service = EmbeddingService(settings=_build_settings("test-key"))

    result = service.embed_texts(["chunk A", "chunk B"])

    assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]


def test_embed_texts_retries_on_429(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeClient:
        call_count = 0

        def __init__(self, timeout: int) -> None:
            self.timeout = timeout

        def __enter__(self) -> "_FakeClient":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def post(self, url: str, headers: dict, json: dict) -> _FakeResponse:
            _FakeClient.call_count += 1
            if _FakeClient.call_count == 1:
                return _FakeResponse(status_code=429, payload={})
            return _FakeResponse(status_code=200, payload={"data": [{"embedding": [0.9, 0.8, 0.7]}]})

    monkeypatch.setattr("app.services.embedding_service.httpx.Client", _FakeClient)
    monkeypatch.setattr("app.services.embedding_service.time.sleep", lambda _: None)

    service = EmbeddingService(settings=_build_settings("test-key"))
    result = service.embed_texts(["query"])

    assert result == [[0.9, 0.8, 0.7]]
    assert _FakeClient.call_count == 2
