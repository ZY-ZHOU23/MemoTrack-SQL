"""
Application configuration settings.
This module defines all configuration parameters for the application,
including database connections, security settings, and API configurations.
Settings are loaded from environment variables with fallback defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application metadata
    PROJECT_NAME: str = "Personal Memo System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database and cache connections
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://user:password@localhost:3306/personal_memo")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings for frontend communication
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True

# Create global settings instance
settings = Settings() 