from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hasty Feedback System"
    PROJECT_VERSION: str = "2.0.0"
    
    DATABASE_URL: str = "sqlite://./feedback.db"
    
    API_V1_STR: str = "/api/v1"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()