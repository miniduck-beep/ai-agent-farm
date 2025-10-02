"""
AI Agent Farm - Celery Background Tasks
=======================================
Полноценная интеграция с Celery 5.4.0 для асинхронной обработки задач
"""

import os
import logging
import traceback
from datetime import datetime
from celery import Celery, Task
from celery.signals import worker_ready
from app.config import settings

# Настройка логирования
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Создание Celery приложения
celery_app = Celery(
    "ai_agent_farm",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks"]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.celery_task_timeout,
    task_soft_time_limit=settings.celery_task_timeout - 60,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    task_routes={
        "app.tasks.run_research_task": {"queue": "research"},
        "app.tasks.run_showcase_analysis": {"queue": "showcase"},
    },
    task_annotations={
        "app.tasks.run_research_task": {"rate_limit": "10/m"},
        "app.tasks.run_showcase_analysis": {"rate_limit": "5/m"},
    }
)

class CallbackTask(Task):
    """Базовый класс задач с обратными вызовами для обновления статуса"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Вызывается при успешном завершении задачи"""
        logger.info(f"Task {task_id} completed successfully")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Вызывается при неудачном завершении задачи"""
        logger.error(f"Task {task_id} failed: {exc}")
        # Обновляем статус задачи в Redis
        try:
            update_task_status(task_id, "failed", error=str(exc))
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")

def update_task_status(task_id: str, status: str, progress: int = 0, result=None, error=None):
    """Обновляет статус задачи в Redis"""
    import redis
    
    try:
        redis_client = redis.Redis.from_url(settings.redis_url)
        task_data = {
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "updated_at": datetime.utcnow().isoformat(),
        }
        
        if result:
            task_data["result"] = result
        if error:
            task_data["error"] = error
            
        redis_client.hset(f"task:{task_id}", mapping=task_data)
        redis_client.expire(f"task:{task_id}", 3600)  # TTL 1 час
        
    except Exception as e:
        logger.error(f"Failed to update task status in Redis: {e}")

@celery_app.task(bind=True, base=CallbackTask, name="app.tasks.run_research_task")
def run_research_task(self, task_id: str, topic: str, crew_type: str, language: str = "ru", depth: str = "standard"):
    """
    Celery задача для выполнения исследования с помощью CrewAI агентов
    
    Args:
        task_id (str): Уникальный идентификатор задачи
        topic (str): Тема исследования  
        crew_type (str): Тип команды агентов
        language (str): Язык анализа (по умолчанию русский)
        depth (str): Глубина анализа
        
    Returns:
        dict: Результат исследования
    """
    try:
        logger.info(f"Starting research task {task_id}: {topic} ({crew_type})")
        
        # Обновляем статус на "обработка"
        update_task_status(task_id, "processing", progress=10)
        self.update_state(state="PROGRESS", meta={"progress": 10, "status": "Инициализация агентов..."})
        
        # Импорт внутри задачи для избежания циклических импортов
        from app.main_crew import CrewFactory
        
        # Создаем фабрику команд
        factory = CrewFactory()
        
        # Обновляем прогресс
        update_task_status(task_id, "processing", progress=30)
        self.update_state(state="PROGRESS", meta={"progress": 30, "status": "Создание команды агентов..."})
        
        # Выполняем исследование в зависимости от типа команды
        logger.info(f"Running {crew_type} crew for task {task_id}")
        
        if crew_type == "business":
            result = factory.run_business_analysis(topic, language, depth)
        elif crew_type == "technical":
            result = factory.run_technical_analysis(topic, language, depth)  
        elif crew_type == "financial":
            result = factory.run_financial_analysis(topic, language, depth)
        elif crew_type == "swot":
            result = factory.run_swot_analysis(topic, language)
        elif crew_type == "investment":
            result = factory.run_investment_analysis(topic, language)
        elif crew_type == "code_review":
            result = factory.run_code_review(topic, language)
        else:
            result = factory.run_business_analysis(topic, language, depth)  # По умолчанию
            
        # Обновляем прогресс
        update_task_status(task_id, "processing", progress=90)
        self.update_state(state="PROGRESS", meta={"progress": 90, "status": "Финализация результатов..."})
        
        # Завершаем задачу
        update_task_status(task_id, "completed", progress=100, result=result)
        
        logger.info(f"Research task {task_id} completed successfully")
        return {
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        error_msg = f"Task {task_id} failed: {str(e)}"
        logger.error(f"{error_msg}\\n{traceback.format_exc()}")
        
        # Обновляем статус на ошибку
        update_task_status(task_id, "failed", error=error_msg)
        self.update_state(state="FAILURE", meta={"error": error_msg})
        
        raise self.retry(exc=e, countdown=60, max_retries=3)

@celery_app.task(bind=True, base=CallbackTask, name="app.tasks.run_showcase_analysis")
def run_showcase_analysis(self, task_id: str, analysis_type: str, data: dict, language: str = "ru"):
    """
    Celery задача для выполнения специализированных анализов (SWOT, инвестиционный, технический)
    
    Args:
        task_id (str): Уникальный идентификатор задачи
        analysis_type (str): Тип анализа (swot, investment, technical_review)
        data (dict): Данные для анализа
        language (str): Язык анализа
        
    Returns:
        dict: Результат специализированного анализа
    """
    try:
        logger.info(f"Starting showcase analysis {task_id}: {analysis_type}")
        
        # Обновляем статус
        update_task_status(task_id, "processing", progress=15)
        self.update_state(state="PROGRESS", meta={"progress": 15, "status": "Подготовка специализированного анализа..."})
        
        from app.main_crew import CrewFactory
        
        factory = CrewFactory()
        
        # Выполняем анализ в зависимости от типа
        if analysis_type == "swot":
            company_name = data.get("company_name", "")
            result = factory.run_swot_analysis(company_name, language)
            
        elif analysis_type == "investment":
            asset_name = data.get("asset_name", "")
            result = factory.run_investment_analysis(asset_name, language)
            
        elif analysis_type == "technical_review":
            repo_url = data.get("repo_url", "")
            result = factory.run_code_review(repo_url, language)
            
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        
        # Завершаем задачу
        update_task_status(task_id, "completed", progress=100, result=result)
        
        logger.info(f"Showcase analysis {task_id} completed successfully")
        return {
            "task_id": task_id,
            "status": "completed", 
            "analysis_type": analysis_type,
            "result": result,
            "completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        error_msg = f"Showcase analysis {task_id} failed: {str(e)}"
        logger.error(f"{error_msg}\\n{traceback.format_exc()}")
        
        update_task_status(task_id, "failed", error=error_msg)
        self.update_state(state="FAILURE", meta={"error": error_msg})
        
        raise self.retry(exc=e, countdown=60, max_retries=2)

@celery_app.task(bind=True, name="app.tasks.health_check")
def health_check(self):
    """Проверка здоровья Celery worker"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "worker_id": self.request.hostname
    }

@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    """Обработчик готовности worker"""
    logger.info("Celery worker is ready and waiting for tasks")

# Функции для совместимости с существующим кодом
def run_research_task_sync(task_id: str, topic: str, crew_type: str, language: str, depth: str):
    """Синхронная версия для локального тестирования"""
    return run_research_task.delay(task_id, topic, crew_type, language, depth)

# Экспорт для использования в других модулях  
__all__ = ["celery_app", "run_research_task", "run_showcase_analysis", "health_check", "update_task_status"]
