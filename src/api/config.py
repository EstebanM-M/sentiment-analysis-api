"""
Application configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_TITLE: str = "Sentiment Analysis API"
    API_VERSION: str = "0.2.0"
    API_DESCRIPTION: str = """
    A production-ready sentiment analysis API using state-of-the-art Transformer models.
    
    ## Features
    * **Fast**: Built with FastAPI for high performance
    * **Accurate**: Uses pre-trained DistilBERT model (95% accuracy)
    * **Scalable**: Supports batch processing
    * **Well-documented**: Interactive API documentation with Swagger UI
    
    ## Endpoints
    * `/api/v1/analyze` - Analyze single text
    * `/api/v1/batch-analyze` - Analyze multiple texts
    * `/api/v1/health` - Health check
    """
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Model Configuration
    MODEL_NAME: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MODEL_CACHE_DIR: str = "./models"
    MAX_LENGTH: int = 512
    
    # Database Configuration (for Day 3)
    DATABASE_URL: str = "sqlite:///./sentiment_analysis.db"
    DB_ECHO: bool = False
    
    # API Security (optional)
    API_KEY: Optional[str] = None
    ENABLE_API_KEY: bool = False
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
