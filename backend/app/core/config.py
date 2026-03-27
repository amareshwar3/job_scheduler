from functools import lru_cache
import re

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Job Scheduler Backend"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/job_scheduler_db"
    db_schema: str = "job_scheduler"
    db_echo: bool = False
    cors_origins: list[str] | str = Field(default_factory=lambda: ["http://localhost:3000"])
    queue_default_priority: int = 100
    queue_default_max_attempts: int = 3

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value: list[str] | str) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    @field_validator("db_schema")
    @classmethod
    def validate_db_schema(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("DB_SCHEMA cannot be empty.")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", cleaned):
            raise ValueError("DB_SCHEMA must be a valid PostgreSQL identifier.")
        return cleaned


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
