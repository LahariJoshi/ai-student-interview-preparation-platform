from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Student Interview Preparation Platform"
    API_V1_STR: str = "/api/v1"

    # Environment: development, staging, production
    ENVIRONMENT: str = "development"

    # Database
    # Default to PostgreSQL connection string; fallback to local SQLite async if env not set
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "interview_prep_db"
    DATABASE_URL: Optional[str] = None

    # Security & JWT
    SECRET_KEY: str = "SUPER_SECRET_KEY_FOR_JWT_DEV_MODE_CHANGE_IN_PROD_123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Cookie Security Settings
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = False  # Set to True in production (HTTPS)
    COOKIE_SAMESITE: str = "lax"  # 'lax', 'strict', or 'none'
    COOKIE_DOMAIN: Optional[str] = None

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Email / SMTP Settings for Password Recovery & Notifications
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: str = "InterviewReady AI"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    RESET_TOKEN_EXPIRE_MINUTES: int = 15

    # Safe Development Password Recovery Key (Never active in production)
    DEV_RECOVERY_KEY: str = "InterviewReadyDev2026!"

    # File Storage Settings
    UPLOADS_DIR: str = "uploads/resumes"

    # ATS Scoring Component Weights (Centralized & Configurable)
    ATS_WEIGHT_FORMAT: float = 0.25
    ATS_WEIGHT_KEYWORD: float = 0.35
    ATS_WEIGHT_SEMANTIC: float = 0.25
    ATS_WEIGHT_IMPACT: float = 0.15

    # Mock Interview Settings
    INTERVIEW_AUDIO_DIR: str = "uploads/interview_audio"
    MAX_AUDIO_SIZE_MB: int = 15
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "auto"  # auto, openai, gemini, offline

    model_config = SettingsConfigDict(
        env_file=(Path(__file__).resolve().parent.parent.parent / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def is_development(self) -> bool:
        """
        Check if backend is running in a local development/testing environment.
        """
        return self.ENVIRONMENT.lower() in ("development", "dev", "local", "test")

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{quote_plus(self.POSTGRES_PASSWORD)}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
