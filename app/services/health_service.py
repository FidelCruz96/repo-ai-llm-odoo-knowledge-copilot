from __future__ import annotations

import socket
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
import psycopg

from app.core.config import Settings, get_settings
from app.models.schemas import HealthResponse


@dataclass
class HealthService:
    settings: Settings

    def run_checks(self) -> HealthResponse:
        checks = {
            "vector_store": self._check_vector_store(),
            "llm_api": self._check_llm_api(),
            "cache": self._check_cache(),
        }
        status = "degraded" if any(value == "error" for value in checks.values()) else "healthy"
        return HealthResponse(
            status=status,
            version=self.settings.app_version,
            checks=checks,
        )

    def _check_vector_store(self) -> str:
        database_url = self.settings.database_url
        if not database_url:
            return "not_configured"

        conn_url = database_url.replace("postgresql+psycopg://", "postgresql://")

        try:
            with psycopg.connect(conn_url, connect_timeout=self.settings.request_timeout_s) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    cur.fetchone()
            return "ok"
        except Exception:
            return "error"

    def _check_llm_api(self) -> str:
        if not self.settings.openai_api_key or self.settings.openai_api_key == "replace_me":
            return "not_configured"

        url = f"{self.settings.openai_base_url.rstrip('/')}/models"
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        timeout = self.settings.request_timeout_s

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url, headers=headers)
                return "ok" if response.status_code == 200 else "error"
        except Exception:
            return "error"

    def _check_cache(self) -> str:
        redis_url = self.settings.redis_url
        if not redis_url:
            return "not_configured"

        parsed = urlparse(redis_url)
        host = parsed.hostname
        port = parsed.port or 6379
        if not host:
            return "error"

        try:
            with socket.create_connection((host, port), timeout=self.settings.request_timeout_s):
                return "ok"
        except OSError:
            return "error"


def get_health_service() -> HealthService:
    return HealthService(settings=get_settings())
