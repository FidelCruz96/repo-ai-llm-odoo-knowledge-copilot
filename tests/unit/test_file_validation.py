from __future__ import annotations

import pytest

from app.utils.file_validation import validate_ingest_file


def test_validate_ingest_file_ok() -> None:
    validate_ingest_file("manual.md", b"contenido", max_size_mb=1)


def test_validate_ingest_file_rejects_extension() -> None:
    with pytest.raises(ValueError, match="Unsupported file extension"):
        validate_ingest_file("manual.exe", b"contenido", max_size_mb=1)


def test_validate_ingest_file_rejects_empty() -> None:
    with pytest.raises(ValueError, match="File is empty"):
        validate_ingest_file("manual.txt", b"", max_size_mb=1)


def test_validate_ingest_file_rejects_oversize() -> None:
    oversized = b"a" * (2 * 1024 * 1024)
    with pytest.raises(ValueError, match="File too large"):
        validate_ingest_file("manual.txt", oversized, max_size_mb=1)
