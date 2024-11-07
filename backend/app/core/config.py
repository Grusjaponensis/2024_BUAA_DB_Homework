from typing import Annotated, Any

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_settings import BaseSettings

from app.mysql_config import *


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    PROJECT_NAME: str = "2024_BUAA_DB_Project"
    
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "b3683501dec4f58e6b06befb551793a2471e37af857240fc8800dff9f3a3693a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_HOST: str = "http://localhost:8000"
    FRONTEND_HOST: str = "http://localhost:3000"
    
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    # API versions
    API_V1_STR: str = "/api/v1"
    
    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]
    
    @property
    def MYSQL_DATABASE_URI(self) -> str:
        """Create a database connection address string."""
        if any(var is None for var in [mysql_user, mysql_password, mysql_host, mysql_db_schema]):
            raise ValueError("Please set your own mysql_user and other variables in ../mysql_config.py")
        return f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db_schema}"
    
    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    DEFAULT_USER_AVATAR_URL: str = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    UPLOAD_AVATAR_FOLDER: str = "app/static/avatars"
    
settings = Settings()