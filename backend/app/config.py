"""Application settings, loaded from the .env file."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8005

    @property
    def input_dir(self) -> Path:
        return PROJECT_ROOT / "input"

    @property
    def frontend_dir(self) -> Path:
        return PROJECT_ROOT / "frontend"


settings = Settings()
