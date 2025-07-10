try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "ScholarDock API"
    app_version: str = "2.0.0"
    debug: bool = False
    
    database_url: str = "sqlite+aiosqlite:///../data/scholar.db"
    
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    google_scholar_base_url: str = "https://scholar.google.com"
    request_delay: float = 5.0
    max_retries: int = 3
    timeout: int = 30
    
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    max_search_results: int = 1000
    results_per_page: int = 10
    
    selenium_driver_path: Optional[str] = None
    use_selenium_fallback: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()