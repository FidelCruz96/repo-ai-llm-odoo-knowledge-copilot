from __future__ import annotations

import httpx
import pytest

from app.core.config import Settings
from app.services.llm_service import LLMService, _format_context


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("POST", "http://test/chat/completions")
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


def test_generate_answer_requires_openai_key() -> None:
    service = LLMService(settings=_build_settings("replace_me"))
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is not configured"):
        service.generate_answer(query="hola", context_chunks=[{"content": "contexto"}])


def test_generate_answer_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeClient:
        def __init__(self, timeout: int) -> None:
            self.timeout = timeout

        def __enter__(self) -> "_FakeClient":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def post(self, url: str, headers: dict, json: dict) -> _FakeResponse:
            assert url.endswith("/chat/completions")
            assert headers["Authorization"].startswith("Bearer ")
            assert json["model"] == "gpt-4o-mini"
            assert json["messages"][1]["content"].find("Question:\nQue es picking?") != -1
            return _FakeResponse(
                status_code=200,
                payload={
                    "choices": [
                        {
                            "message": {"content": "  Es un movimiento de stock.  "},
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {"total_tokens": 42},
                    "model": "gpt-4o-mini",
                },
            )

    monkeypatch.setattr("app.services.llm_service.httpx.Client", _FakeClient)
    service = LLMService(settings=_build_settings("test-key"))

    result = service.generate_answer(
        query="Que es picking?",
        context_chunks=[
            {"doc_name": "inventory.md", "page": 1, "content": "Un picking representa un movimiento de stock."}
        ],
    )

    assert result.answer == "Es un movimiento de stock."
    assert result.tokens_used == 42
    assert result.finish_reason == "stop"
    assert result.model == "gpt-4o-mini"


def test_format_context_handles_empty_and_page_optional() -> None:
    assert _format_context([]) == "No context available."

    formatted = _format_context(
        [
            {"doc_name": "a.md", "page": 2, "content": "  A  "},
            {"doc_name": "b.md", "page": None, "content": "B"},
        ]
    )
    assert "[1] a.md, page 2\nA" in formatted
    assert "[2] b.md\nB" in formatted
