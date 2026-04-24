from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.sql import SQL

from app.core.config import Settings, get_settings
from app.models.db_models import EmbeddedChunkRecord


@dataclass
class VectorService:
    settings: Settings

    def ping(self) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    cur.fetchone()
            return True
        except Exception:
            return False

    def ensure_schema(self) -> None:
        dimensions = int(self.settings.embedding_dimensions)
        if dimensions <= 0:
            raise ValueError("EMBEDDING_DIMENSIONS must be greater than 0")

        ddl = f"""
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS documents_chunks (
            id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL,
            doc_name TEXT NOT NULL,
            source_type TEXT NOT NULL,
            page INTEGER,
            module TEXT,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding vector({dimensions}) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_documents_chunks_doc_id ON documents_chunks (doc_id);
        CREATE INDEX IF NOT EXISTS idx_documents_chunks_module ON documents_chunks (module);
        """
        with self._connect(autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)

    def upsert_chunks(self, chunks: list[EmbeddedChunkRecord]) -> None:
        if not chunks:
            return

        self.ensure_schema()
        query = """
        INSERT INTO documents_chunks (
            id, doc_id, doc_name, source_type, page, module, chunk_index, content, embedding
        )
        VALUES (
            %(id)s, %(doc_id)s, %(doc_name)s, %(source_type)s, %(page)s,
            %(module)s, %(chunk_index)s, %(content)s, %(embedding)s::vector
        )
        ON CONFLICT (id) DO UPDATE SET
            doc_id = EXCLUDED.doc_id,
            doc_name = EXCLUDED.doc_name,
            source_type = EXCLUDED.source_type,
            page = EXCLUDED.page,
            module = EXCLUDED.module,
            chunk_index = EXCLUDED.chunk_index,
            content = EXCLUDED.content,
            embedding = EXCLUDED.embedding;
        """
        payload = [
            {
                "id": chunk.id,
                "doc_id": chunk.doc_id,
                "doc_name": chunk.doc_name,
                "source_type": chunk.source_type,
                "page": chunk.page,
                "module": chunk.module,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "embedding": _to_pgvector_literal(chunk.embedding),
            }
            for chunk in chunks
        ]

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, payload)
            conn.commit()

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        self.ensure_schema()
        where_parts = []
        params: dict[str, Any] = {
            "query_embedding": _to_pgvector_literal(query_embedding),
            "top_k": top_k,
        }
        if filters:
            if module := filters.get("module"):
                where_parts.append(SQL("module = %(module)s"))
                params["module"] = module
            if doc_id := filters.get("doc_id"):
                where_parts.append(SQL("doc_id = %(doc_id)s"))
                params["doc_id"] = doc_id

        where_clause = SQL("WHERE ") + SQL(" AND ").join(where_parts) if where_parts else SQL("")
        query = SQL(
            """
        SELECT
            id,
            doc_id,
            doc_name,
            source_type,
            page,
            module,
            chunk_index,
            content,
            1 - (embedding <=> %(query_embedding)s::vector) AS score
        FROM documents_chunks
        {where_clause}
        ORDER BY embedding <=> %(query_embedding)s::vector
        LIMIT %(top_k)s;
        """
        ).format(where_clause=where_clause)

        with self._connect() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return list(cur.fetchall())

    def _connect(self, autocommit: bool = False) -> psycopg.Connection:
        conn_url = self.settings.database_url.replace("postgresql+psycopg://", "postgresql://")
        return psycopg.connect(conn_url, connect_timeout=self.settings.request_timeout_s, autocommit=autocommit)


def _to_pgvector_literal(embedding: list[float]) -> str:
    return "[" + ",".join(f"{value:.10f}" for value in embedding) + "]"


def get_vector_service() -> VectorService:
    return VectorService(settings=get_settings())
