# config/settings.py
from __future__ import annotations
from pydantic import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):
    safetyculture_base_url: str = Field(
        default="https://api.safetyculture.io", description="Base URL API"
    )
    safetyculture_token: str = Field(..., description="Bearer token API")
    output_dir: Path = Field(default=Path("output"))
    # filtros opcionales para /audits/search
    modified_after: str | None = None   # ISO8601 (UTC), ej. "2025-01-01T00:00:00Z"
    modified_before: str | None = None
    include_archived: bool = False
    templates: list[str] = Field(default_factory=list)  # IDs de template a filtrar

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
