from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "Vacation Vista Chatbot"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    DUFFEL_API_KEY: str
    GEMINI_API_KEY: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SENDER_EMAIL: EmailStr

    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index: Optional[str] = None


    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"

    @property
    def GEMINI_MODEL_URL(self) -> str:
        return (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self.GEMINI_API_KEY}"
        )

settings = Settings()
