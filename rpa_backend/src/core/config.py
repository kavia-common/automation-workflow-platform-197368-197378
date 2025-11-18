import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rpa.db")

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS
    _cors_origins_env = os.getenv("CORS_ORIGINS", "")
    CORS_ORIGINS: List[str] = (
        [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
        if _cors_origins_env
        else ["*"]
    )

    # App metadata
    PROJECT_NAME: str = "RPA Backend"
    API_VERSION: str = "0.1.0"
    DESCRIPTION: str = "Backend for RPA platform handling workflows, bots, schedules, and auth."


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings instance."""
    return Settings()
