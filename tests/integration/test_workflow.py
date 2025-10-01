"""Integration тесты для полного workflow исследований."""

import pytest
from unittest.mock import Mock, patch
import time


@pytest.mark.integration
def test_complete_research_workflow(client, sample_research_data, mock_llm, mock_celery):
    """Тест полного цикла исследования от создания до получения результата."""
    
    # Мокаем задачу Celery
    mock_task = Mock()
    mock_task.id = "integration-test-123"
    mock_celery.send_task.return_value = mock_task
    
    # 1. Создаем исследование
    response = client.post(
        "/research",
        json=sample_research_data["basic_request"]
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["task_id"]
    
    # 2. Мокаем завершенную задачу
    mock_result = Mock()
    mock_result.state = "SUCCESS"
    mock_result.result = "# Исследование\n\nДетальный отчет..."
    mock_result.info = {"progress": 100}
    mock_celery.AsyncResult.return_value = mock_result
    
    # 3. Получаем результат
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    
    result_data = response.json()
    assert result_data["status"] == "SUCCESS"
    assert result_data["progress"] == 100
    assert "result" in result_data


@pytest.mark.integration
@patch('app.agents.create_crew')
def test_agent_team_integration(mock_create_crew, client, sample_research_data):
    """Тест интеграции с системой агентов."""
    
    # Мокаем создание команды агентов
    mock_crew = Mock()
    mock_crew.kickoff.return_value = "Mock research result"
    mock_create_crew.return_value = mock_crew
    
    response = client.post(
        "/research",
        json=sample_research_data["advanced_request"]
    )
    
    assert response.status_code == 200
    # Проверяем, что была создана команда нужного типа
    mock_create_crew.assert_called_once()
