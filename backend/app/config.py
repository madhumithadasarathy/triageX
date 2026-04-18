"""
TriageX Configuration Module
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    APP_NAME: str = "TriageX"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-Powered Visual Medical Triage Assistant"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./triagex.db"

    # JWT Auth
    SECRET_KEY: str = "triagex-super-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # AI / LLM (Optional - Online Mode)
    OPENAI_API_KEY: Optional[str] = None
    LLM_ENABLED: bool = False

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    REPORTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

# Ensure reports directory exists
os.makedirs(settings.REPORTS_DIR, exist_ok=True)
