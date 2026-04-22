from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from uuid import uuid4

from app.core.config import Settings, get_settings
from app.models.schemas import QueryRequest, QueryResponse, SourceItem
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.services.llm_service import LLMService, get_llm_service
from app.services.vector_service import VectorService, get_vector_service


@dataclass
class RagService:
    settings: Settings
    embedding_service: EmbeddingService
    vector_service: VectorService
    llm_service: LLMService

    def answer_query(self, query_request: QueryRequest) -> QueryResponse:
        started_at = perf_counter()
        trace_id = str(uuid4())

        query_embedding = self.embedding_service.embed_query(query_request.query)
        raw_chunks = self.vector_service.search(
            query_embedding=query_embedding,
            top_k=self.settings.top_k,
            filters=query_request.filters,
        )

        filtered_chunks = [
            chunk
            for chunk in raw_chunks
            if float(chunk.get("score", 0.0)) >= self.settings.similarity_threshold
        ]

        if filtered_chunks:
            llm_result = self.llm_service.generate_answer(
                query=query_request.query,
                context_chunks=filtered_chunks,
            )
            answer = llm_result.answer or "No se pudo generar una respuesta con el contexto recuperado."
            tokens_used = llm_result.tokens_used
        else:
            answer = "No encontré suficiente contexto para responder con precisión."
            tokens_used = None

        sources = [
            SourceItem(
                doc_id=str(chunk.get("doc_id", "")),
                doc_name=str(chunk.get("doc_name", "")),
                page=chunk.get("page"),
                score=float(chunk.get("score", 0.0)),
            )
            for chunk in filtered_chunks
        ]
        latency_ms = (perf_counter() - started_at) * 1000

        return QueryResponse(
            answer=answer,
            sources=sources,
            tokens_used=tokens_used,
            latency_ms=round(latency_ms, 2),
            trace_id=trace_id,
        )


def get_rag_service() -> RagService:
    return RagService(
        settings=get_settings(),
        embedding_service=get_embedding_service(),
        vector_service=get_vector_service(),
        llm_service=get_llm_service(),
    )
