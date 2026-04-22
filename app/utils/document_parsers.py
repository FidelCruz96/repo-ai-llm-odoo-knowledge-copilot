from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass(slots=True)
class ParsedPage:
    page: int | None
    text: str


def parse_document_bytes(content: bytes, filename: str) -> list[ParsedPage]:
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return _parse_pdf(content)
    if suffix in {".md", ".markdown", ".txt"}:
        text = content.decode("utf-8", errors="ignore").strip()
        return [ParsedPage(page=None, text=text)] if text else []

    raise ValueError(f"Unsupported file type: {suffix or 'unknown'}")


def _parse_pdf(content: bytes) -> list[ParsedPage]:
    pages: list[ParsedPage] = []
    with fitz.open(stream=content, filetype="pdf") as document:
        for index, page in enumerate(document, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append(ParsedPage(page=index, text=text))
    return pages
