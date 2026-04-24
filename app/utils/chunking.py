from __future__ import annotations

from app.models.db_models import ChunkRecord
from app.utils.document_parsers import ParsedPage


def split_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    clean_text = text.strip()
    if not clean_text:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    total = len(clean_text)

    while start < total:
        end = min(start + chunk_size, total)
        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= total:
            break
        start = end - overlap

    return chunks


def build_chunks(
    pages: list[ParsedPage],
    doc_id: str,
    doc_name: str,
    source_type: str,
    module: str | None,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[ChunkRecord]:
    chunk_records: list[ChunkRecord] = []
    chunk_counter = 0

    for parsed_page in pages:
        for chunk_text in split_text(parsed_page.text, chunk_size=chunk_size, overlap=overlap):
            chunk_counter += 1
            page_number = parsed_page.page or 0
            chunk_records.append(
                ChunkRecord(
                    id=f"{doc_id}-p{page_number}-c{chunk_counter:04d}",
                    doc_id=doc_id,
                    doc_name=doc_name,
                    source_type=source_type,
                    page=parsed_page.page,
                    module=module,
                    chunk_index=chunk_counter,
                    content=chunk_text,
                )
            )

    return chunk_records
