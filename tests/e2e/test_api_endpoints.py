"""End-to-end тесты API endpoints."""

import pytest
import time
from unittest.mock import patch


@pytest.mark.e2e
def test_api_health_check(client):
    """E2E тест проверки работоспособности API."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert isinstance(data["status"], str)


@pytest.mark.e2e 
def test_full_api_flow(client):
    """E2E тест полного потока работы API."""
    
    # Проверяем статус системы
    status_response = client.get("/status")
    assert status_response.status_code == 200
    
    with patch('app.tasks.celery_app') as mock_celery:
        # Мокаем Celery задачу
        mock_task = Mock()
        mock_task.id = "e2e-test-task"
        mock_celery.send_task.return_value = mock_task
        
        # Создаем исследование
        research_response = client.post(
            "/research",
            json={"topic": "E2E Test Topic"}
        )
        assert research_response.status_code == 200
        
        task_data = research_response.json()
        assert "task_id" in task_data
        
        # Мокаем результат
        mock_result = Mock()
        mock_result.state = "SUCCESS"
        mock_result.result = "E2E test result"
        mock_result.info = {"progress": 100}
        mock_celery.AsyncResult.return_value = mock_result
        
        # Получаем результат
        result_response = client.get(f"/result/{task_data['task_id']}")
        assert result_response.status_code == 200
        
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"


@pytest.mark.e2e
@pytest.mark.parametrize("crew_type", ["general", "business_analyst", "tech_research"])
def test_different_crew_types(client, crew_type):
    """E2E тест различных типов команд агентов."""
    
    with patch('app.tasks.celery_app') as mock_celery:
        mock_task = Mock()
        mock_task.id = f"crew-test-{crew_type}"
        mock_celery.send_task.return_value = mock_task
        
        response = client.post(
            "/research",
            json={
                "topic": f"Test topic for {crew_type}",
                "crew_type": crew_type
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "PENDING"
