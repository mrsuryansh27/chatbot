from dotenv import load_dotenv
load_dotenv()

import os
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    # App
    APP_NAME: str = "Vacation Vista Chatbot"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    # Database
    DATABASE_URL: str

    # Provisioning
    MASTER_API_KEY: str

    # Third-party
    DUFFEL_API_KEY: Optional[str] = None
    GEMINI_MODEL_URL: Optional[str] = None

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    SENDER_EMAIL: Optional[EmailStr] = None

    # Vector store
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENV: Optional[str] = None
    PINECONE_INDEX: Optional[str] = None

settings = Settings()

# Clean DATABASE_URL for asyncpg (strip sslmode, add +asyncpg)
raw = settings.DATABASE_URL
p = urlparse(raw)
q = [(k, v) for k, v in parse_qsl(p.query) if k.lower() != 'sslmode']
s = p.scheme
if s.startswith('postgresql') and '+asyncpg' not in s:
    s = s.replace('postgresql', 'postgresql+asyncpg', 1)
DATABASE_URL = urlunparse((s, p.netloc, p.path, p.params, urlencode(q), p.fragment))
