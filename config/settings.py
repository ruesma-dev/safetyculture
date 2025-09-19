# config/settings.py
from __future__ import annotations

import json
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del microservicio (cargada desde .env por defecto)."""

    # ── SafetyCulture API ─────────────────────────────────────────────────
    safetyculture_base_url: str = Field(
        default="https://api.safetyculture.io",
        env="SAFETYCULTURE_BASE_URL",
        description="Base URL de la API de SafetyCulture",
    )
    safetyculture_token: str = Field(
        ...,
        env="SAFETYCULTURE_TOKEN",
        description="Bearer token de SafetyCulture",
    )

    # ── Salida ───────────────────────────────────────────────────────────
    output_dir: Path = Field(
        default=Path("output"),
        env="OUTPUT_DIR",
        description="Directorio de salida para ficheros CSV",
    )

    # ── Filtros opcionales para /audits/search ───────────────────────────
    modified_after: str | None = Field(default=None, env="MODIFIED_AFTER")   # ISO8601 UTC
    modified_before: str | None = Field(default=None, env="MODIFIED_BEFORE")
    include_archived: bool = Field(default=False, env="INCLUDE_ARCHIVED")
    # Acepta JSON '["tpl1","tpl2"]' o CSV 'tpl1,tpl2'
    templates: list[str] = Field(default_factory=list, env="TEMPLATES")

    # ── Configuración del cargador de entorno (.env) ─────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Normalizadores ───────────────────────────────────────────────────
    @field_validator("templates", mode="before")
    @classmethod
    def _parse_templates(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            # intenta JSON; si falla, trata como CSV
            try:
                return json.loads(s)
            except Exception:
                return [x.strip() for x in s.split(",") if x.strip()]
        return v
