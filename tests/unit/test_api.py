"""Unit тесты для API endpoints."""

import pytest
from unittest.mock import Mock, patch


def test_root_endpoint(client):
    """Тест корневого endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "AI Agent Farm is running!"


def test_status_endpoint(client):
    """Тест endpoint статуса системы."""
    with patch('app.api.get_system_status') as mock_status:
        mock_status.return_value = {
            "redis": "connected",
            "celery": "running",
            "agents": "ready"
        }
        
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "redis" in data
        assert "celery" in data


def test_research_endpoint_basic(client, sample_research_data, mock_celery):
    """Тест создания базового исследования."""
    mock_task = Mock()
    mock_task.id = "test-task-123"
    mock_celery.send_task.return_value = mock_task
    
    response = client.post(
        "/research",
        json=sample_research_data["basic_request"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data
    assert data["status"] == "PENDING"


def test_research_endpoint_validation(client):
    """Тест валидации параметров исследования."""
    # Пустая тема
    response = client.post(
        "/research", 
        json={"topic": ""}
    )
    assert response.status_code == 422
    
    # Отсутствующая тема
    response = client.post(
        "/research",
        json={}
    )
    assert response.status_code == 422


def test_result_endpoint(client, mock_celery):
    """Тест получения результата исследования."""
    task_id = "test-task-123"
    
    # Мокаем результат задачи
    mock_result = Mock()
    mock_result.state = "SUCCESS"
    mock_result.result = "Test research result"
    mock_celery.AsyncResult.return_value = mock_result
    
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    assert "status" in data
    assert data["task_id"] == task_id


def test_result_endpoint_not_found(client, mock_celery):
    """Тест получения результата несуществующей задачи."""
    mock_result = Mock()
    mock_result.state = "PENDING"
    mock_result.result = None
    mock_celery.AsyncResult.return_value = mock_result
    
    response = client.get("/result/nonexistent-task")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "PENDING"
