from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.config import Settings, get_settings
from app.models.db_models import EmbeddedChunkRecord
from app.models.schemas import IngestResponse, IngestedDocument
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.services.vector_service import VectorService, get_vector_service
from app.utils.chunking import build_chunks
from app.utils.document_parsers import parse_document_bytes
from app.utils.ids import build_doc_id


@dataclass
class IngestService:
    settings: Settings
    embedding_service: EmbeddingService
    vector_service: VectorService

    def ingest_files(self, files: list[tuple[str, bytes]], module: str | None = None) -> IngestResponse:
        ingested: list[IngestedDocument] = []

        for filename, content in files:
            parsed_pages = parse_document_bytes(content=content, filename=filename)
            source_type = Path(filename).suffix.lower().lstrip(".") or "unknown"
            doc_id = build_doc_id(filename)
            chunk_records = build_chunks(
                pages=parsed_pages,
                doc_id=doc_id,
                doc_name=filename,
                source_type=source_type,
                module=module,
                chunk_size=self.settings.chunk_size,
                overlap=self.settings.chunk_overlap,
            )
            if not chunk_records:
                ingested.append(IngestedDocument(file=filename, chunks=0, status="empty"))
                continue

            embeddings = self.embedding_service.embed_texts([chunk.content for chunk in chunk_records])
            embedded_chunks: list[EmbeddedChunkRecord] = []
            for chunk, embedding in zip(chunk_records, embeddings, strict=True):
                embedded_chunks.append(
                    EmbeddedChunkRecord(
                        id=chunk.id,
                        doc_id=chunk.doc_id,
                        doc_name=chunk.doc_name,
                        source_type=chunk.source_type,
                        page=chunk.page,
                        module=chunk.module,
                        chunk_index=chunk.chunk_index,
                        content=chunk.content,
                        embedding=embedding,
                    )
                )

            self.vector_service.upsert_chunks(embedded_chunks)
            ingested.append(IngestedDocument(file=filename, chunks=len(embedded_chunks), status="ok"))

        return IngestResponse(ingested=ingested)


def get_ingest_service() -> IngestService:
    return IngestService(
        settings=get_settings(),
        embedding_service=get_embedding_service(),
        vector_service=get_vector_service(),
    )
