from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="odoo-knowledge-copilot", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    api_key: str = Field(default="change-me", alias="API_KEY")

    database_url: str = Field(
        default="postgresql://odoo:odoo@postgres:5432/odoo_knowledge",
        alias="DATABASE_URL",
    )
    redis_url: str | None = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    model_name: str = Field(default="gpt-4o-mini", alias="MODEL_NAME")
    embedding_model: str = Field(default="text-embedding-3-large", alias="EMBEDDING_MODEL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_base_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_BASE_URL")

    top_k: int = Field(default=5, alias="TOP_K")
    similarity_threshold: float = Field(default=0.75, alias="SIMILARITY_THRESHOLD")
    chunk_size: int = Field(default=800, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=100, alias="CHUNK_OVERLAP")
    embedding_dimensions: int = Field(default=3072, alias="EMBEDDING_DIMENSIONS")

    request_timeout_s: int = Field(default=5, alias="REQUEST_TIMEOUT_S")
    rate_limit_per_minute: int = Field(default=30, alias="RATE_LIMIT_PER_MINUTE")
    max_upload_size_mb: int = Field(default=10, alias="MAX_UPLOAD_SIZE_MB")


@lru_cache
def get_settings() -> Settings:
    return Settings()
