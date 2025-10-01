from celery import Celery
from app.main_crew import create_research_crew
import redis
import json
from datetime import datetime

# Настраиваем Celery с backend для хранения результатов
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'  # ВАЖНО: Backend для хранения результатов
)

# Подключение к Redis для дополнительного логирования
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def update_task_status(task_id, status, message, progress=None):
    """Обновление статуса задачи в Redis для детального мониторинга"""
    try:
        status_data = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'progress': progress
        }
        redis_client.setex(f'task-status-{task_id}', 3600, json.dumps(status_data))
    except Exception as e:
        print(f"Ошибка обновления статуса: {e}")

@celery_app.task(bind=True, name="run_research_crew")
def run_research_crew(self, topic):
    """
    Главная задача Celery для запуска исследования через команду агентов.
    
    Args:
        topic (str): Тема для исследования
    
    Returns:
        str: Готовый структурированный отчет
    """
    task_id = self.request.id
    
    try:
        print(f"🚀 [ЗАДАЧА] Celery worker получил задачу: Исследовать тему '{topic}'")
        print(f"🆔 [ЗАДАЧА] ID: {task_id}")
        
        # Статус 1: Инициализация (5%)
        update_task_status(task_id, 'INITIALIZING', 'Инициализация системы агентов...', 5)
        self.update_state(
            state='PROGRESS', 
            meta={'status': 'Инициализация системы агентов...', 'current': 5, 'total': 100}
        )
        
        # Статус 2: Запуск агентов (10%)
        update_task_status(task_id, 'STARTING', 'Запуск команды ИИ-агентов...', 10)
        self.update_state(
            state='PROGRESS', 
            meta={'status': 'Запуск команды ИИ-агентов...', 'current': 10, 'total': 100}
        )
        
        # Статус 3: Исследование (30%)
        update_task_status(task_id, 'RESEARCHING', 'Агент-исследователь ищет информацию в интернете...', 30)
        self.update_state(
            state='PROGRESS', 
            meta={'status': 'Поиск и анализ информации...', 'current': 30, 'total': 100}
        )
        
        # Запуск основной работы команды агентов
        print(f"🎯 [ЗАДАЧА] Запуск create_research_crew для темы: '{topic}'")
        result = create_research_crew(topic)
        
        # Статус 4: Финализация (95%)
        update_task_status(task_id, 'FINALIZING', 'Формирование итогового отчета...', 95)
        self.update_state(
            state='PROGRESS', 
            meta={'status': 'Завершение исследования...', 'current': 95, 'total': 100}
        )
        
        # Статус 5: Завершено (100%)
        update_task_status(task_id, 'COMPLETED', 'Исследование завершено успешно!', 100)
        
        print(f"✅ [ЗАДАЧА] Celery worker завершил задачу по теме '{topic}'")
        print(f"📄 [РЕЗУЛЬТАТ] Длина отчета: {len(result)} символов")
        
        # Возвращаем результат (он автоматически сохранится в Redis backend)
        return result
        
    except Exception as e:
        error_msg = f"Ошибка при выполнении исследования: {str(e)}"
        print(f"❌ [ЗАДАЧА] {error_msg}")
        
        # Статус: Ошибка
        update_task_status(task_id, 'ERROR', error_msg, 0)
        
        # Обновляем состояние в Celery
        self.update_state(
            state='FAILURE',
            meta={'status': error_msg, 'current': 0, 'total': 100, 'error': str(e)}
        )
        
        # Перевыбрасываем исключение для корректной обработки в Celery
        raise e

# Настройки Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,  # Результаты хранятся 1 час
)
