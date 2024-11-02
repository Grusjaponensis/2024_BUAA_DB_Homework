from pydantic_settings import BaseSettings

from app.mysql_config import *

class Settings(BaseSettings):
    PROJECT_NAME: str = "2024_BUAA_DB_Project"
    
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "b3683501dec4f58e6b06befb551793a2471e37af857240fc8800dff9f3a3693a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_HOST: str = "http://localhost:8000"
    FRONTEND_HOST: str | None = None # FIXME
    
    # API versions
    API_V1_STR: str = "/api/v1"
    
    @property
    def MYSQL_DATABASE_URI(self) -> str:
        """Create a database connection address string."""
        if mysql_user is None:
            raise ValueError("Please set your own mysql_user and other variables in ../mysql_config.py")
        return f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db_schema}"
    
    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
settings = Settings()