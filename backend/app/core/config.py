from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    APP_NAME: str = "AIQYN AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Email via Resend (optional — if empty, codes print to Railway logs)
    RESEND_API_KEY: Optional[str] = None

    model_config = {
        "env_file": str(_ENV_FILE) if _ENV_FILE.exists() else None,
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
