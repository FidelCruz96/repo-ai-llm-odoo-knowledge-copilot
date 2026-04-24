from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.config import Settings, get_settings


@dataclass(slots=True)
class LLMResult:
    answer: str
    tokens_used: int | None
    model: str
    finish_reason: str | None = None


@dataclass
class LLMService:
    settings: Settings

    def generate_answer(self, query: str, context_chunks: list[dict]) -> LLMResult:
        if not self.settings.openai_api_key or self.settings.openai_api_key == "replace_me":
            raise RuntimeError("OPENAI_API_KEY is not configured")

        context_text = _format_context(context_chunks=context_chunks)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Odoo technical assistant. "
                    "Answer only with the provided context. "
                    "If context is insufficient, state it clearly."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{query}\n\n"
                    f"Context:\n{context_text}\n\n"
                    "Respond in concise Spanish."
                ),
            },
        ]

        url = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.model_name,
            "messages": messages,
            "temperature": 0.2,
        }

        with httpx.Client(timeout=self.settings.request_timeout_s) as client:
            response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        body = response.json()
        choices = body.get("choices", [])
        choice = choices[0] if choices else {}
        message = choice.get("message", {})
        usage = body.get("usage", {})

        return LLMResult(
            answer=(message.get("content") or "").strip(),
            tokens_used=usage.get("total_tokens"),
            model=body.get("model") or self.settings.model_name,
            finish_reason=choice.get("finish_reason"),
        )


def _format_context(context_chunks: list[dict]) -> str:
    if not context_chunks:
        return "No context available."

    lines: list[str] = []
    for index, chunk in enumerate(context_chunks, start=1):
        doc_name = chunk.get("doc_name") or "unknown"
        page = chunk.get("page")
        page_label = f", page {page}" if page is not None else ""
        content = (chunk.get("content") or "").strip()
        lines.append(f"[{index}] {doc_name}{page_label}\n{content}")
    return "\n\n".join(lines)


def get_llm_service() -> LLMService:
    return LLMService(settings=get_settings())
