from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseSettings, validator, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_PORT: str
    EMAILS_ENABLED: bool = False
    EMAIL_TEMPLATES_DIR: str = "app/templates"
    PROJECT_NAME: str = "shop"
    SMTP_TLS: bool = True
    SERVER_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(
            cls,
            v: Optional[str],
            values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
