from dataclasses import dataclass


@dataclass(slots=True)
class ChunkRecord:
    id: str
    doc_id: str
    doc_name: str
    source_type: str
    page: int | None
    module: str | None
    chunk_index: int
    content: str


@dataclass(slots=True)
class EmbeddedChunkRecord(ChunkRecord):
    embedding: list[float]
