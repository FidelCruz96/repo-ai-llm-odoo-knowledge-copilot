from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from app.core.config import Settings, get_settings


@dataclass
class EmbeddingService:
    settings: Settings

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        if not self.settings.openai_api_key or self.settings.openai_api_key == "replace_me":
            raise RuntimeError("OPENAI_API_KEY is not configured")

        url = f"{self.settings.openai_base_url.rstrip('/')}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        payload = {"model": self.settings.embedding_model, "input": texts}
        timeout = self.settings.request_timeout_s

        attempt = 0
        max_retries = 3

        while True:
            try:
                with httpx.Client(timeout=timeout) as client:
                    response = client.post(url, headers=headers, json=payload)
                if response.status_code == 429 and attempt < max_retries:
                    wait_s = 2 ** attempt
                    time.sleep(wait_s)
                    attempt += 1
                    continue
                response.raise_for_status()
                data = response.json().get("data", [])
                return [item["embedding"] for item in data]
            except httpx.HTTPError:
                if attempt < max_retries:
                    wait_s = 2 ** attempt
                    time.sleep(wait_s)
                    attempt += 1
                    continue
                raise


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(settings=get_settings())
