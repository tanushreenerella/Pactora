from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_base_url: str = "https://api-m.sandbox.paypal.com"

    openai_api_key: str = ""

    database_url: str = "postgresql+psycopg://pactora:pactora@localhost:5432/pactora"

    # Comma-separated list of extra allowed origins (e.g. the deployed frontend URL).
    cors_origins: str = ""

    @property
    def allowed_origins(self) -> list[str]:
        extra = [o.strip().rstrip("/") for o in self.cors_origins.split(",") if o.strip()]
        return ["http://localhost:3000", "http://127.0.0.1:3000", *extra]


@lru_cache
def get_settings() -> Settings:
    return Settings()
