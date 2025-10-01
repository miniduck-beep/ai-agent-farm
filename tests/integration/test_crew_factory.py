"""
Integration Tests - Crew Factory
===============================
Интеграционные тесты фабрики команд агентов
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.main_crew import CrewFactory, run_research, create_dynamic_tasks


@pytest.mark.integration
class TestCrewFactory:
    """Тесты фабрики команд агентов"""
    
    def test_crew_factory_initialization(self, mock_llm, mock_tools):
        """Тест инициализации фабрики команд"""
        factory = CrewFactory()
        
        assert factory.llm is not None
        assert factory.tools is not None
    
    @patch('app.main_crew.Agent')
    @patch('app.main_crew.Crew')
    def test_create_general_crew(self, mock_crew_class, mock_agent_class, mock_llm, mock_tools):
        """Тест создания универсальной команды"""
        factory = CrewFactory()
        
        # Мокаем агентов
        mock_agent_class.return_value = Mock()
        mock_crew_instance = Mock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = factory.create_general_crew()
        
        # Проверяем что создано правильное количество агентов
        assert mock_agent_class.call_count == 2  # Исследователь + Писатель
        mock_crew_class.assert_called_once()
        assert crew == mock_crew_instance
    
    @patch('app.main_crew.Agent')
    @patch('app.main_crew.Crew')
    def test_create_business_analysis_crew(self, mock_crew_class, mock_agent_class, mock_llm, mock_tools):
        """Тест создания команды бизнес-аналитики"""
        factory = CrewFactory()
        
        mock_agent_class.return_value = Mock()
        mock_crew_instance = Mock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = factory.create_business_analysis_crew()
        
        # Проверяем что создано 3 агента для бизнес-анализа
        assert mock_agent_class.call_count == 3  # Аналитик + Финансист + Стратег
        mock_crew_class.assert_called_once()
    
    @patch('app.main_crew.Agent')
    @patch('app.main_crew.Crew')  
    def test_all_crew_types_creation(self, mock_crew_class, mock_agent_class, mock_llm, mock_tools):
        """Тест создания всех типов команд"""
        factory = CrewFactory()
        mock_agent_class.return_value = Mock()
        mock_crew_class.return_value = Mock()
        
        crew_methods = [
            factory.create_general_crew,
            factory.create_business_analysis_crew,
            factory.create_seo_content_crew,
            factory.create_tech_research_crew,
            factory.create_financial_analysis_crew
        ]
        
        for create_method in crew_methods:
            mock_agent_class.reset_mock()
            mock_crew_class.reset_mock()
            
            crew = create_method()
            
            assert crew is not None
            assert mock_agent_class.called
            assert mock_crew_class.called


@pytest.mark.integration
class TestDynamicTasks:
    """Тесты создания динамических задач"""
    
    def test_create_tasks_general_crew(self, mock_crew):
        """Тест создания задач для универсальной команды"""
        mock_crew.agents = [Mock(), Mock()]  # 2 агента
        
        tasks = create_dynamic_tasks(
            crew=mock_crew,
            topic="Test topic",
            crew_type="general",
            language="ru", 
            depth="standard"
        )
        
        assert len(tasks) == 2  # Исследователь + Писатель
        assert mock_crew.tasks == tasks
        
        # Проверяем содержание задач
        for task in tasks:
            assert hasattr(task, 'description')
            assert hasattr(task, 'agent')
            assert hasattr(task, 'expected_output')
    
    def test_create_tasks_business_analysis_crew(self, mock_crew):
        """Тест создания задач для команды бизнес-аналитики"""
        mock_crew.agents = [Mock(), Mock(), Mock()]  # 3 агента
        
        tasks = create_dynamic_tasks(
            crew=mock_crew,
            topic="Market analysis",
            crew_type="business_analysis",
            language="en",
            depth="comprehensive"
        )
        
        assert len(tasks) == 3  # Аналитик + Финансист + Стратег
        
        # Проверяем что задачи содержат правильные инструкции
        task_descriptions = [task.description for task in tasks]
        assert any("рынка" in desc for desc in task_descriptions)
        assert any("финансовый анализ" in desc for desc in task_descriptions)
        assert any("стратегические рекомендации" in desc for desc in task_descriptions)
    
    def test_create_tasks_depth_variations(self, mock_crew):
        """Тест создания задач с разной глубиной анализа"""
        mock_crew.agents = [Mock(), Mock()]
        
        depths = ["basic", "standard", "comprehensive"]
        
        for depth in depths:
            tasks = create_dynamic_tasks(
                crew=mock_crew,
                topic="Test topic",
                crew_type="general",
                depth=depth
            )
            
            # Проверяем что глубина влияет на описание задач
            for task in tasks:
                if depth == "basic":
                    assert "краткий анализ" in task.description
                elif depth == "comprehensive":
                    assert "исчерпывающий анализ" in task.description


@pytest.mark.integration
class TestResearchExecution:
    """Тесты выполнения исследований"""
    
    @patch('app.main_crew.crew_factory')
    def test_run_research_general(self, mock_factory, mock_llm, mock_tools):
        """Тест запуска общего исследования"""
        # Мокаем фабрику и команду
        mock_crew = Mock()
        mock_crew.kickoff.return_value = "Test research result"
        mock_factory.create_general_crew.return_value = mock_crew
        
        result = run_research(
            topic="Test research topic",
            crew_type="general",
            language="ru",
            depth="standard"
        )
        
        assert result == "Test research result"
        mock_factory.create_general_crew.assert_called_once()
        mock_crew.kickoff.assert_called_once()
    
    @patch('app.main_crew.crew_factory')
    def test_run_research_business_analysis(self, mock_factory, mock_llm, mock_tools):
        """Тест запуска бизнес-анализа"""
        mock_crew = Mock()
        mock_crew.kickoff.return_value = "Business analysis result"
        mock_factory.create_business_analysis_crew.return_value = mock_crew
        
        result = run_research(
            topic="Market analysis",
            crew_type="business_analysis", 
            language="en",
            depth="comprehensive"
        )
        
        assert result == "Business analysis result"
        mock_factory.create_business_analysis_crew.assert_called_once()
    
    @patch('app.main_crew.crew_factory')
    def test_run_research_invalid_crew_type(self, mock_factory, mock_llm, mock_tools):
        """Тест запуска с недопустимым типом команды"""
        mock_crew = Mock()
        mock_crew.kickoff.return_value = "Default crew result"
        mock_factory.create_general_crew.return_value = mock_crew
        
        result = run_research(
            topic="Test topic",
            crew_type="invalid_type"  # Недопустимый тип
        )
        
        # Должна использоваться общая команда по умолчанию
        assert result == "Default crew result"
        mock_factory.create_general_crew.assert_called_once()
    
    @patch('app.main_crew.crew_factory')
    def test_run_research_error_handling(self, mock_factory, mock_llm, mock_tools):
        """Тест обработки ошибок при выполнении исследования"""
        mock_crew = Mock()
        mock_crew.kickoff.side_effect = Exception("Research execution failed")
        mock_factory.create_general_crew.return_value = mock_crew
        
        with pytest.raises(Exception, match="Research execution failed"):
            run_research(topic="Test topic")
