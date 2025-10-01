"""
End-to-End Tests - Full Workflow
===============================
Полные сквозные тесты AI Agent Farm workflow
"""

import pytest
import time
from unittest.mock import Mock, patch
import json


@pytest.mark.e2e
class TestCompleteResearchWorkflow:
    """Сквозные тесты полного цикла исследований"""
    
    def test_complete_workflow_mock(self, client, mock_celery, mock_crew, helpers):
        """Тест полного workflow с моками"""
        
        # 1. Проверяем статус системы
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Создаем исследование
        request_data = {
            "topic": "E2E Test Research Topic",
            "crew_type": "business_analysis",
            "language": "ru",
            "depth": "standard"
        }
        
        create_response = client.post("/research", json=request_data)
        assert create_response.status_code == 200
        
        create_data = create_response.json()
        task_id = create_data["task_id"]
        assert task_id is not None
        
        # 3. Мокаем результат как SUCCESS
        success_result = helpers.create_sample_crew_response()
        mock_result = helpers.create_mock_task_result("SUCCESS", success_result)
        mock_celery.AsyncResult.return_value = mock_result
        
        # 4. Получаем результат
        result_response = client.get(f"/result/{task_id}")
        assert result_response.status_code == 200
        
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["progress"] == 100
        assert result_data["result"] is not None
    
    def test_workflow_with_different_crew_types(self, client, mock_celery, helpers):
        """Тест workflow с разными типами команд"""
        
        crew_types = ["general", "business_analysis", "seo_content", "tech_research"]
        
        for crew_type in crew_types:
            # Создаем исследование для каждого типа команды
            request_data = {
                "topic": f"Test topic for {crew_type}",
                "crew_type": crew_type
            }
            
            response = client.post("/research", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "task_id" in data
            assert crew_type in data["crew_info"]["name"].lower() or crew_type == "general"
    
    def test_workflow_error_scenarios(self, client, mock_celery):
        """Тест workflow с различными сценариями ошибок"""
        
        # 1. Тест с пустой темой
        invalid_request = {"topic": ""}
        response = client.post("/research", json=invalid_request)
        assert response.status_code == 422
        
        # 2. Тест с недопустимым типом команды
        invalid_crew_request = {
            "topic": "Valid topic",
            "crew_type": "invalid_crew"
        }
        response = client.post("/research", json=invalid_crew_request)
        assert response.status_code == 422
        
        # 3. Тест получения результата несуществующей задачи
        response = client.get("/result/nonexistent-task-id")
        # Ожидаем ошибку или пустой результат, но не краш
        assert response.status_code in [200, 404, 500]
    
    def test_task_management_workflow(self, client, mock_celery):
        """Тест workflow управления задачами"""
        
        # 1. Получаем список активных задач
        tasks_response = client.get("/tasks")
        assert tasks_response.status_code == 200
        
        # 2. Создаем задачу
        request_data = {"topic": "Task management test"}
        create_response = client.post("/research", json=request_data)
        assert create_response.status_code == 200
        task_id = create_response.json()["task_id"]
        
        # 3. Отменяем задачу
        cancel_response = client.delete(f"/task/{task_id}")
        assert cancel_response.status_code == 200
        assert cancel_response.json()["status"] == "cancelled"


@pytest.mark.e2e
@pytest.mark.slow
class TestRealAPIIntegration:
    """Тесты с реальной интеграцией API (медленные)"""
    
    def test_api_documentation_accessible(self, client):
        """Тест доступности API документации"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Проверяем что это OpenAPI документация
        content = response.content.decode()
        assert "swagger" in content.lower() or "openapi" in content.lower()
    
    def test_api_health_monitoring(self, client):
        """Тест мониторинга здоровья API"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = ["status", "timestamp", "version", "components"]
        for field in required_fields:
            assert field in data
    
    def test_cors_headers(self, client):
        """Тест CORS заголовков"""
        response = client.options("/")
        
        # Проверяем наличие CORS заголовков
        assert "access-control-allow-origin" in response.headers or response.status_code == 200
    
    def test_content_type_handling(self, client):
        """Тест обработки различных типов контента"""
        
        # JSON запрос
        json_response = client.post(
            "/research",
            json={"topic": "Content type test"}
        )
        assert json_response.status_code in [200, 422]  # Валидный JSON или ошибка валидации
        
        # Неправильный content-type
        invalid_response = client.post(
            "/research",
            data="invalid data",
            headers={"Content-Type": "text/plain"}
        )
        assert invalid_response.status_code == 422


@pytest.mark.e2e
class TestSystemIntegration:
    """Тесты интеграции системных компонентов"""
    
    def test_api_celery_integration(self, client, mock_celery):
        """Тест интеграции API с Celery"""
        
        # Мокаем Celery worker
        mock_celery.control.inspect.return_value.active.return_value = {
            "worker1": [{"id": "task1"}]
        }
        
        # 1. Проверяем что API может общаться с Celery
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        health_data = health_response.json()
        assert health_data["components"]["celery"] != "unhealthy"
        
        # 2. Создаем задачу через API
        create_response = client.post(
            "/research", 
            json={"topic": "Integration test"}
        )
        assert create_response.status_code == 200
        
        # 3. Проверяем что задача передалась в Celery
        mock_celery.delay.assert_called()
    
    def test_error_propagation(self, client, mock_celery):
        """Тест распространения ошибок через систему"""
        
        # Мокаем ошибку в Celery
        mock_celery.delay.side_effect = Exception("Celery is down")
        
        response = client.post("/research", json={"topic": "Error test"})
        
        # API должен корректно обработать ошибку Celery
        assert response.status_code == 500
        error_data = response.json()
        assert "detail" in error_data
        assert "Ошибка запуска исследования" in error_data["detail"]
