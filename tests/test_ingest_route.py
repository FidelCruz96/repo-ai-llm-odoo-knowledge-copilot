import asyncio

import pytest
from fastapi import HTTPException

from app.api.routes_ingest import ingest_documents
from app.main import app
from app.models.schemas import IngestResponse, IngestedDocument


class FakeIngestService:
    def __init__(self) -> None:
        self.captured_files: list[tuple[str, bytes]] = []
        self.captured_module: str | None = None

    def ingest_files(self, files: list[tuple[str, bytes]], module: str | None = None) -> IngestResponse:
        self.captured_files = files
        self.captured_module = module
        return IngestResponse(ingested=[IngestedDocument(file=files[0][0], chunks=1, status="ok")])


class FakeUploadFile:
    def __init__(self, filename: str, content: bytes) -> None:
        self.filename = filename
        self._content = content

    async def read(self) -> bytes:
        return self._content


def test_ingest_route_is_registered() -> None:
    paths = {route.path for route in app.routes}
    assert "/v1/ingest" in paths


def test_ingest_documents_function_uses_service() -> None:
    fake_service = FakeIngestService()
    upload = FakeUploadFile(filename="manual.txt", content=b"Odoo test content")

    response = asyncio.run(
        ingest_documents(
            files=[upload],
            module="inventory",
            service=fake_service,
        )
    )

    assert response.ingested[0].file == "manual.txt"
    assert fake_service.captured_module == "inventory"
    assert fake_service.captured_files[0][1] == b"Odoo test content"


def test_ingest_documents_rejects_unsupported_extension() -> None:
    fake_service = FakeIngestService()
    upload = FakeUploadFile(filename="manual.exe", content=b"Odoo test content")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            ingest_documents(
                files=[upload],
                module="inventory",
                service=fake_service,
            )
        )

    assert exc_info.value.status_code == 400
    assert "Unsupported file extension" in str(exc_info.value.detail)
