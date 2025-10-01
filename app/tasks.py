"""
AI Agent Farm - Enhanced Celery Tasks
====================================
Асинхронные задачи с поддержкой различных команд агентов
"""

from celery import Celery
from app.config import settings
import logging
import time

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
def research_task(self, topic: str, crew_type: str = "general", language: str = "ru", depth: str = "standard"):
    """
    Выполняет исследование с использованием выбранной команды агентов
    
    Args:
        topic: Тема для исследования
        crew_type: Тип команды агентов
        language: Язык результата
        depth: Глубина анализа
    
    Returns:
        dict: Результат исследования
    """
    start_time = time.time()
    
    try:
        logger.info(f"🔍 Начинаем исследование: {topic} (команда: {crew_type}, язык: {language}, глубина: {depth})")
        
        # Обновляем прогресс
        self.update_state(
            state='PROGRESS', 
            meta={
                'current': 10, 
                'total': 100, 
                'status': f'Инициализация команды {crew_type}...',
                'crew_type': crew_type
            }
        )
        
        # Импортируем здесь чтобы избежать circular imports
        from app.main_crew import run_research
        
        # Обновляем прогресс
        self.update_state(
            state='PROGRESS', 
            meta={
                'current': 25, 
                'total': 100, 
                'status': 'Поиск и анализ информации...',
                'crew_type': crew_type
            }
        )
        
        # Запускаем исследование с выбранной командой
        result = run_research(
            topic=topic,
            crew_type=crew_type, 
            language=language,
            depth=depth
        )
        
        # Обновляем прогресс 
        self.update_state(
            state='PROGRESS', 
            meta={
                'current': 90, 
                'total': 100, 
                'status': 'Финализация отчета...',
                'crew_type': crew_type
            }
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"✅ Исследование завершено: {topic} ({processing_time:.2f}s)")
        
        return {
            'status': 'completed',
            'result': result,
            'topic': topic,
            'crew_type': crew_type,
            'language': language,
            'depth': depth,
            'processing_time': processing_time,
            'message': f'Исследование успешно завершено командой {crew_type}'
        }
        
    except Exception as exc:
        processing_time = time.time() - start_time
        logger.error(f"❌ Ошибка в исследовании {topic}: {str(exc)}")
        
        self.update_state(
            state='FAILURE',
            meta={
                'current': 100, 
                'total': 100, 
                'status': f'Ошибка: {str(exc)}',
                'processing_time': processing_time,
                'crew_type': crew_type
            }
        )
        
        raise exc

@celery_app.task
def health_check():
    """Проверка работоспособности Celery worker"""
    return {
        'status': 'healthy', 
        'message': 'Celery worker is running',
        'timestamp': time.time()
    }

if __name__ == '__main__':
    celery_app.start()
