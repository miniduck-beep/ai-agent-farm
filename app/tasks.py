"""
AI Agent Farm - Celery Tasks
============================
Асинхронные задачи для многоагентных исследований
"""

from celery import Celery
from app.config import settings
import logging

# Настройка логирования
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# 🔧 Конфигурация Celery из переменных окружения
celery_app = Celery(
    'ai_agent_farm',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=['app.tasks']
)

# ⚙️ Конфигурация Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=settings.celery_task_timeout,
    task_soft_time_limit=settings.celery_task_timeout - 300,  # 5 минут до жесткого лимита
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
)

@celery_app.task(bind=True)
def research_task(self, topic: str, **kwargs):
    """
    Выполняет исследование с использованием многоагентной системы
    
    Args:
        topic: Тема для исследования
        **kwargs: Дополнительные параметры (language, depth, etc.)
    
    Returns:
        dict: Результат исследования
    """
    try:
        logger.info(f"🔍 Начинаем исследование: {topic}")
        
        # Обновляем прогресс
        self.update_state(state='PROGRESS', meta={'current': 10, 'total': 100, 'status': 'Инициализация агентов...'})
        
        # Импортируем здесь чтобы избежать circular imports
        from app.main_crew import run_research
        
        # Обновляем прогресс
        self.update_state(state='PROGRESS', meta={'current': 25, 'total': 100, 'status': 'Поиск информации...'})
        
        # Запускаем исследование
        result = run_research(topic, **kwargs)
        
        # Обновляем прогресс 
        self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100, 'status': 'Финализация отчета...'})
        
        logger.info(f"✅ Исследование завершено: {topic}")
        
        return {
            'status': 'completed',
            'result': result,
            'topic': topic,
            'message': 'Исследование успешно завершено'
        }
        
    except Exception as exc:
        logger.error(f"❌ Ошибка в исследовании {topic}: {str(exc)}")
        
        self.update_state(
            state='FAILURE',
            meta={'current': 100, 'total': 100, 'status': f'Ошибка: {str(exc)}'}
        )
        
        raise exc

@celery_app.task
def health_check():
    """Проверка работоспособности Celery worker"""
    return {'status': 'healthy', 'message': 'Celery worker is running'}

if __name__ == '__main__':
    celery_app.start()
