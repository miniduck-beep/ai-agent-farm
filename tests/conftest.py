"""
AI Agent Farm Test Configuration
================================
Общие настройки и фикстуры для тестов
"""

import pytest
import asyncio
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import tempfile
import os

# Импорты для тестирования
from app.api import app
from app.config import settings
from app.tasks import celery_app


@pytest.fixture
def client() -> TestClient:
    """Создает тестовый клиент FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Мок настроек для тестов"""
    with patch('app.config.settings') as mock:
        mock.google_api_key = "test_google_key"
        mock.serper_api_key = "test_serper_key"
        mock.redis_url = "redis://localhost:6379/1"
        mock.debug = True
        mock.log_level = "INFO"
        yield mock


@pytest.fixture
def mock_celery():
    """Мок Celery для изоляции тестов"""
    with patch('app.api.celery_app') as mock:
        mock_task = Mock()
        mock_task.id = "test-task-id-123"
        mock.AsyncResult.return_value = mock_task
        
        # Настройка mock для research_task.delay
        with patch('app.api.research_task') as mock_research:
            mock_research.delay.return_value = mock_task
            yield mock


@pytest.fixture
def mock_llm():
    """Мок LLM для избежания реальных API вызовов"""
    with patch('app.main_crew.get_llm') as mock:
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Test LLM response")
        mock.return_value = mock_llm
        yield mock_llm


@pytest.fixture
def mock_tools():
    """Мок инструментов для агентов"""
    with patch('app.main_crew.get_tools') as mock:
        mock_tool = Mock()
        mock_tool.run.return_value = "Test tool result"
        mock.return_value = [mock_tool]
        yield mock


@pytest.fixture
def mock_crew():
    """Мок CrewAI для тестов"""
    with patch('app.main_crew.Crew') as mock:
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Test research result"
        mock.return_value = mock_crew_instance
        yield mock_crew_instance


@pytest.fixture
def sample_research_data() -> Dict[str, Any]:
    """Образцы данных для тестов"""
    return {
        "basic_request": {
            "topic": "Тестирование AI систем",
            "crew_type": "general",
            "language": "ru", 
            "depth": "standard"
        },
        "advanced_request": {
            "topic": "Анализ рынка блокчейн технологий",
            "crew_type": "business_analysis",
            "language": "en",
            "depth": "comprehensive"
        },
        "invalid_request": {
            "topic": "",  # Пустая тема
            "crew_type": "invalid_type"
        }
    }


@pytest.fixture
def temp_env():
    """Создает временные переменные окружения"""
    original_env = {}
    test_env = {
        'GOOGLE_API_KEY': 'test_google_key',
        'SERPER_API_KEY': 'test_serper_key',
        'REDIS_URL': 'redis://localhost:6379/1',
        'DEBUG': 'true'
    }
    
    # Сохраняем оригинальные значения
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    yield test_env
    
    # Восстанавливаем оригинальные значения
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def mock_redis():
    """Мок Redis для тестов"""
    with patch('redis.Redis') as mock:
        mock_instance = Mock()
        mock_instance.ping.return_value = True
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для асинхронных тестов"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# Helpers для тестов
class TestHelpers:
    """Вспомогательные функции для тестов"""
    
    @staticmethod
    def create_mock_task_result(status: str = "SUCCESS", result: str = "Test result"):
        """Создает мок результата Celery задачи"""
        mock_result = Mock()
        mock_result.status = status
        mock_result.result = result
        mock_result.info = {"progress": 100}
        return mock_result
    
    @staticmethod
    def create_sample_crew_response():
        """Создает образец ответа от команды агентов"""
        return {
            "status": "completed",
            "result": "# Test Research Report\n\nThis is a test research result.",
            "topic": "Test Topic",
            "crew_type": "general",
            "processing_time": 45.67
        }


@pytest.fixture
def helpers():
    """Предоставляет доступ к helper функциям"""
    return TestHelpers


# Маркеры для категоризации тестов
def pytest_configure(config):
    """Конфигурация pytest с кастомными маркерами"""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (deselect with '-m \"not unit\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
