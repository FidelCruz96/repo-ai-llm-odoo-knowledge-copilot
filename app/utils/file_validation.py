from __future__ import annotations

from pathlib import Path


ALLOWED_EXTENSIONS = {".pdf", ".md", ".markdown", ".txt"}


def validate_ingest_file(filename: str, content: bytes, max_size_mb: int) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension: {extension or 'unknown'}. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    if not content:
        raise ValueError(f"File is empty: {filename}")

    max_size_bytes = max_size_mb * 1024 * 1024
    if len(content) > max_size_bytes:
        raise ValueError(f"File too large: {filename}. Max size: {max_size_mb} MB")
