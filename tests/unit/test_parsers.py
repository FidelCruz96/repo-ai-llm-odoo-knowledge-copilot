from __future__ import annotations

import fitz
import pytest

from app.utils.document_parsers import parse_document_bytes


def test_parse_txt_document() -> None:
    pages = parse_document_bytes(b"Linea uno\nLinea dos", "manual.txt")

    assert len(pages) == 1
    assert pages[0].page is None
    assert "Linea uno" in pages[0].text


def test_parse_markdown_document() -> None:
    pages = parse_document_bytes(b"# Titulo\nContenido", "manual.md")

    assert len(pages) == 1
    assert pages[0].page is None
    assert "Titulo" in pages[0].text


def test_parse_pdf_document() -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Texto PDF de prueba")
    payload = document.tobytes()
    document.close()

    pages = parse_document_bytes(payload, "manual.pdf")

    assert len(pages) == 1
    assert pages[0].page == 1
    assert "Texto PDF" in pages[0].text


def test_parse_unsupported_file_type() -> None:
    with pytest.raises(ValueError, match="Unsupported file type"):
        parse_document_bytes(b"contenido", "manual.docx")
