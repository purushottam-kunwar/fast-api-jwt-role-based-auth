from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Role Based Access Control Auth Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "ba9dc3f976cf8fb40519dcd152a8d7d21c0b7861d841711cdb2602be8e85fd7c")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    USERS_OPEN_REGISTRATION: str = os.environ.get("USERS_OPEN_REGISTRATION", "True")

    ENVIRONMENT: Optional[str]

    FIRST_SUPER_ADMIN_EMAIL: str = os.environ.get("FIRST_SUPER_ADMIN_EMAIL", "superadmin@email.com")
    FIRST_SUPER_ADMIN_PASSWORD: str = os.environ.get("FIRST_SUPER_ADMIN_PASSWORD", "superdupersecretpassword")
    FIRST_SUPER_ADMIN_ACCOUNT_NAME: str = os.environ.get("FIRST_SUPER_ADMIN_ACCOUNT_NAME", "superduperaccount")

    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_USER: str = os.environ.get("DB_USER", "pk")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "pk")
    DB_NAME: str = os.environ.get("DB_NAME", "jwt")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
