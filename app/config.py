"""
AI Agent Farm Configuration Module
==================================
Централизованная конфигурация с переменными окружения
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Настройки приложения из переменных окружения"""
    
    # 🚀 API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 🗄️ Redis Configuration  
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_max_connections: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "50"))
    
    # ⚙️ Celery Configuration
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0") 
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    celery_task_timeout: int = int(os.getenv("CELERY_TASK_TIMEOUT", "3600"))
    
    # 🤖 AI API Keys
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    serper_api_key: Optional[str] = os.getenv("SERPER_API_KEY")  
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # 🧠 AI Model Configuration
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))
    gemini_max_tokens: int = int(os.getenv("GEMINI_MAX_TOKENS", "8192"))
    
    # 📊 Logging & Monitoring
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    enable_metrics: bool = os.getenv("ENABLE_METRICS", "false").lower() == "true"
    
    # 🔒 Security Settings
    api_key_required: bool = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    # 🌐 CORS Settings
    cors_origins: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Глобальный экземпляр настроек
settings = Settings()

# Валидация критичных настроек
def validate_required_settings():
    """Проверяет наличие обязательных настроек"""
    errors = []
    
    if not settings.google_api_key:
        errors.append("GOOGLE_API_KEY is required")
    
    if not settings.serper_api_key:
        errors.append("SERPER_API_KEY is required")
        
    if errors:
        raise ValueError(f"Missing required configuration: {', '.join(errors)}")

# Проверяем при импорте модуля
try:
    validate_required_settings()
except ValueError as e:
    print(f"⚠️  Configuration Warning: {e}")
    print("💡 Please check your .env file and ensure all required API keys are set")
