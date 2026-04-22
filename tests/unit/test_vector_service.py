from __future__ import annotations

from app.models.db_models import EmbeddedChunkRecord
from app.services.vector_service import VectorService, _to_pgvector_literal


def test_to_pgvector_literal() -> None:
    value = _to_pgvector_literal([0.1, 1.5, -2.0])
    assert value.startswith("[")
    assert value.endswith("]")
    assert "," in value


def test_upsert_chunks_empty_does_not_touch_db(test_settings) -> None:
    service = VectorService(settings=test_settings)

    def _should_not_connect(*args, **kwargs):
        raise AssertionError("DB should not be called for empty chunk list")

    service._connect = _should_not_connect  # type: ignore[method-assign]
    service.upsert_chunks([])


def test_ping_returns_false_when_db_fails(test_settings) -> None:
    service = VectorService(settings=test_settings)

    def _raise_error(*args, **kwargs):
        raise RuntimeError("db error")

    service._connect = _raise_error  # type: ignore[method-assign]
    assert service.ping() is False


def test_search_applies_filters(test_settings) -> None:
    executed: dict[str, object] = {}

    class _FakeCursor:
        def __enter__(self) -> "_FakeCursor":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def execute(self, query: str, params: dict) -> None:
            executed["query"] = query
            executed["params"] = params

        def fetchall(self):
            return []

    class _FakeConnection:
        def __enter__(self) -> "_FakeConnection":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def cursor(self, row_factory=None) -> _FakeCursor:
            return _FakeCursor()

    service = VectorService(settings=test_settings)
    service.ensure_schema = lambda: None  # type: ignore[method-assign]
    service._connect = lambda autocommit=False: _FakeConnection()  # type: ignore[method-assign]

    results = service.search(
        query_embedding=[0.1, 0.2, 0.3],
        top_k=3,
        filters={"module": "inventory", "doc_id": "doc-1"},
    )

    assert results == []
    assert "module = %(module)s" in str(executed["query"])
    assert "doc_id = %(doc_id)s" in str(executed["query"])
    params = executed["params"]
    assert isinstance(params, dict)
    assert params["module"] == "inventory"
    assert params["doc_id"] == "doc-1"


def test_upsert_chunks_calls_db_for_non_empty_list(test_settings) -> None:
    captured: dict[str, object] = {"executemany_called": False, "committed": False}

    class _FakeCursor:
        def __enter__(self) -> "_FakeCursor":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def executemany(self, query: str, payload: list[dict]) -> None:
            captured["executemany_called"] = True
            captured["payload"] = payload

    class _FakeConnection:
        def __enter__(self) -> "_FakeConnection":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def cursor(self):
            return _FakeCursor()

        def commit(self) -> None:
            captured["committed"] = True

    service = VectorService(settings=test_settings)
    service.ensure_schema = lambda: None  # type: ignore[method-assign]
    service._connect = lambda autocommit=False: _FakeConnection()  # type: ignore[method-assign]

    chunks = [
        EmbeddedChunkRecord(
            id="doc-1-p1-c0001",
            doc_id="doc-1",
            doc_name="manual.txt",
            source_type="txt",
            page=1,
            module="inventory",
            chunk_index=1,
            content="Texto",
            embedding=[0.1, 0.2, 0.3],
        )
    ]
    service.upsert_chunks(chunks)

    assert captured["executemany_called"] is True
    assert captured["committed"] is True
