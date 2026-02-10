from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    app_name: str = "UILove"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql+asyncpg://uilove:password@localhost:5432/uilove"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_expire_seconds: int = 3600
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Admin
    admin_email: str = "admin@uilove.co"
    admin_password: str = "changeme123"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
