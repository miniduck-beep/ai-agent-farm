"""Общие настройки pytest для тестов AI Agent Farm."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import tempfile
import os

@pytest.fixture
def client():
    """Создает тестовый клиент FastAPI."""
    from app.api import app
    return TestClient(app)

@pytest.fixture  
def mock_celery():
    """Мокает Celery для изоляции тестов."""
    with patch('app.tasks.celery_app') as mock:
        yield mock

@pytest.fixture
def mock_redis():
    """Мокает Redis для изоляции тестов."""
    with patch('redis.Redis') as mock:
        yield mock

@pytest.fixture
def mock_llm():
    """Мокает LLM для избежания реальных API вызовов."""
    with patch('langchain_google_genai.ChatGoogleGenerativeAI') as mock:
        mock_instance = Mock()
        mock_instance.invoke.return_value = Mock(content="Test response")
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def temp_env():
    """Создает временные переменные окружения для тестов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        env_vars = {
            'GOOGLE_API_KEY': 'test_key',
            'SERPER_API_KEY': 'test_serper_key',
            'DEBUG': 'true',
        }
        
        original_vars = {}
        for key, value in env_vars.items():
            original_vars[key] = os.environ.get(key)
            os.environ[key] = value
            
        yield env_vars
        
        # Восстанавливаем оригинальные значения
        for key, original_value in original_vars.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

@pytest.fixture
def sample_research_data():
    """Образцы данных для тестов исследований."""
    return {
        "basic_request": {
            "topic": "Искусственный интеллект в образовании"
        },
        "advanced_request": {
            "topic": "Будущее блокчейн технологий",
            "crew_type": "tech_research",
            "language": "ru",
            "depth": "deep"
        },
        "expected_response": {
            "task_id": "test-task-id-123",
            "status": "PENDING",
            "message": "Исследование принято в работу..."
        }
    }
