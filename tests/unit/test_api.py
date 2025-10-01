"""
Unit Tests - API Endpoints
==========================
Тесты для API эндпоинтов AI Agent Farm
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json


@pytest.mark.unit
class TestAPIEndpoints:
    """Тесты основных API эндпоинтов"""
    
    def test_root_endpoint(self, client):
        """Тест корневого эндпоинта"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "AI Agent Farm is running!"
        assert "version" in data
        assert "available_crews" in data
    
    def test_health_endpoint_healthy(self, client, mock_celery):
        """Тест health эндпоинта при здоровой системе"""
        # Мокаем здоровую систему
        mock_celery.control.inspect.return_value.active.return_value = {"worker1": []}
        mock_celery.broker_connection.return_value.ensure_connection.return_value = None
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "components" in data
        assert data["components"]["api"] == "healthy"
    
    def test_crews_endpoint(self, client):
        """Тест эндпоинта информации о командах"""
        response = client.get("/crews")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_crews" in data
        assert "default" in data
        assert data["default"] == "general"
        
        crews = data["available_crews"]
        assert "general" in crews
        assert "business_analysis" in crews
        assert len(crews) >= 5  # Проверяем что все команды присутствуют


@pytest.mark.unit
class TestResearchEndpoint:
    """Тесты эндпоинта создания исследований"""
    
    def test_create_research_basic(self, client, mock_celery, sample_research_data):
        """Тест создания базового исследования"""
        request_data = sample_research_data["basic_request"]
        
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "PENDING"
        assert "crew_info" in data
        assert "estimated_time" in data
    
    def test_create_research_advanced(self, client, mock_celery, sample_research_data):
        """Тест создания продвинутого исследования"""
        request_data = sample_research_data["advanced_request"]
        
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["crew_info"]["name"] == "Бизнес-аналитика"
        assert "comprehensive" in data["estimated_time"]  # Больше времени для comprehensive
    
    def test_create_research_validation_empty_topic(self, client):
        """Тест валидации пустой темы"""
        request_data = {"topic": ""}
        
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 422  # Validation error
        
    def test_create_research_validation_invalid_crew(self, client):
        """Тест валидации недопустимого типа команды"""
        request_data = {
            "topic": "Test topic",
            "crew_type": "invalid_crew_type"
        }
        
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_research_all_parameters(self, client, mock_celery):
        """Тест создания исследования со всеми параметрами"""
        request_data = {
            "topic": "Comprehensive analysis of AI market",
            "crew_type": "business_analysis",
            "language": "en", 
            "depth": "comprehensive"
        }
        
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["crew_info"]["name"] == "Бизнес-аналитика"


@pytest.mark.unit  
class TestResultEndpoint:
    """Тесты эндпоинта получения результатов"""
    
    def test_get_result_pending(self, client, mock_celery, helpers):
        """Тест получения результата PENDING задачи"""
        task_id = "test-task-pending"
        mock_result = helpers.create_mock_task_result("PENDING", None)
        mock_celery.AsyncResult.return_value = mock_result
        
        response = client.get(f"/result/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING"
        assert data["progress"] == 0
    
    def test_get_result_success(self, client, mock_celery, helpers):
        """Тест получения успешного результата"""
        task_id = "test-task-success"
        mock_result = helpers.create_mock_task_result("SUCCESS", helpers.create_sample_crew_response())
        mock_celery.AsyncResult.return_value = mock_result
        
        response = client.get(f"/result/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["progress"] == 100
        assert data["result"] is not None
    
    def test_get_result_failure(self, client, mock_celery, helpers):
        """Тест получения результата с ошибкой"""
        task_id = "test-task-failure"
        mock_result = helpers.create_mock_task_result("FAILURE", None)
        mock_result.info = "Test error message"
        mock_celery.AsyncResult.return_value = mock_result
        
        response = client.get(f"/result/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "FAILURE"
        assert data["error"] == "Test error message"
    
    def test_get_result_nonexistent_task(self, client, mock_celery):
        """Тест получения результата несуществующей задачи"""
        task_id = "nonexistent-task"
        mock_celery.AsyncResult.side_effect = Exception("Task not found")
        
        response = client.get(f"/result/{task_id}")
        
        assert response.status_code == 500


@pytest.mark.unit
class TestTaskManagement:
    """Тесты управления задачами"""
    
    def test_cancel_task(self, client, mock_celery):
        """Тест отмены задачи"""
        task_id = "test-task-to-cancel"
        
        response = client.delete(f"/task/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"
        mock_celery.control.revoke.assert_called_once_with(task_id, terminate=True)
    
    def test_list_active_tasks(self, client, mock_celery):
        """Тест получения списка активных задач"""
        # Мокаем активные задачи
        mock_celery.control.inspect.return_value.active.return_value = {
            "worker1": [{"id": "task1", "name": "research_task"}]
        }
        mock_celery.control.inspect.return_value.scheduled.return_value = {}
        
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        assert "active_tasks" in data
        assert "total_active" in data
        assert data["total_active"] == 1


@pytest.mark.unit
class TestErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_404_handler(self, client):
        """Тест обработки 404 ошибок"""
        response = client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert data["error"] == "Not Found"
        assert "available_endpoints" in data
    
    def test_internal_error_during_research_creation(self, client, mock_celery):
        """Тест обработки внутренних ошибок при создании исследования"""
        # Мокаем ошибку Celery
        mock_celery.delay.side_effect = Exception("Celery connection failed")
        
        request_data = {"topic": "Test topic"}
        response = client.post("/research", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Ошибка запуска исследования" in data["detail"]
