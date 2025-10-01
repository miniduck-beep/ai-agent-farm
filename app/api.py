"""
AI Agent Farm - Enhanced FastAPI Application  
==========================================
Production-ready API с поддержкой различных типов команд агентов
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import logging
import uuid
from datetime import datetime
import time

from app.config import settings
from app.tasks import research_task, celery_app

# Настройка логирования
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="AI Agent Farm",
    description="🤖 Мощная многоагентная система для автоматизированных исследований и генерации контента",
    version="1.0.0-beta",
    contact={
        "name": "AI Agent Farm Team", 
        "url": "https://github.com/miniduck-beep/ai-agent-farm",
        "email": "support@ai-agent-farm.dev"
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/miniduck-beep/ai-agent-farm/blob/main/LICENSE",
    }
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class ResearchRequest(BaseModel):
    """Модель запроса на исследование"""
    topic: str = Field(..., description="Тема для исследования", min_length=5, max_length=500)
    crew_type: Literal["general", "business_analysis", "seo_content", "tech_research", "financial_analysis"] = Field(
        default="general", 
        description="Тип специализированной команды агентов"
    )
    language: Literal["ru", "en"] = Field(default="ru", description="Язык результата исследования")
    depth: Literal["basic", "standard", "comprehensive"] = Field(
        default="standard", 
        description="Глубина анализа: basic (быстрый), standard (детальный), comprehensive (исчерпывающий)"
    )

class ResearchResponse(BaseModel):
    """Модель ответа при создании исследования"""
    task_id: str = Field(..., description="Уникальный идентификатор задачи")
    status: str = Field(..., description="Текущий статус задачи")
    message: str = Field(..., description="Сообщение о состоянии")
    estimated_time: str = Field(..., description="Примерное время выполнения")
    created_at: datetime = Field(..., description="Время создания задачи")
    crew_info: Dict[str, Any] = Field(..., description="Информация о команде агентов")

class TaskResult(BaseModel):
    """Модель результата выполнения задачи"""
    task_id: str
    status: str
    progress: int = Field(..., ge=0, le=100, description="Прогресс выполнения в процентах")
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class SystemStatus(BaseModel):
    """Модель статуса системы"""
    status: str
    timestamp: datetime
    version: str
    components: Dict[str, str]
    active_tasks: int
    completed_tasks: int

# Информация о типах команд
CREW_TYPE_INFO = {
    "general": {
        "name": "Универсальная команда",
        "description": "Команда из исследователя и технического писателя для общих задач",
        "agents": ["Старший исследователь", "Технический писатель"],
        "best_for": ["Общие исследования", "Обзорные анализы", "Простые темы"]
    },
    "business_analysis": {
        "name": "Бизнес-аналитика",
        "description": "Команда экспертов для глубокого анализа рынков и бизнеса",
        "agents": ["Аналитик рынка", "Финансовый аналитик", "Стратегический консультант"],
        "best_for": ["Анализ рынка", "Конкурентная разведка", "Бизнес-стратегии", "Инвестиционный анализ"]
    },
    "seo_content": {
        "name": "SEO и контент-маркетинг",
        "description": "Специалисты по поисковой оптимизации и контент-стратегиям",
        "agents": ["SEO-эксперт", "Контент-стратег", "Digital-маркетолог"],
        "best_for": ["SEO-аудит", "Контент-планы", "Digital-стратегии", "Продвижение сайтов"]
    },
    "tech_research": {
        "name": "Технические исследования",
        "description": "Команда для анализа технологий и архитектурных решений",
        "agents": ["Технический исследователь", "Архитектор решений", "DevOps инженер"],
        "best_for": ["Технологические тренды", "Архитектурные решения", "Техническая экспертиза"]
    },
    "financial_analysis": {
        "name": "Финансовый анализ",
        "description": "Эксперты по финансовому моделированию и инвестициям",
        "agents": ["Финансовый аналитик", "Аналитик рисков", "Инвестиционный советник"],
        "best_for": ["Финансовое моделирование", "Анализ рисков", "Инвестиционные решения"]
    }
}

# Эндпоинты
@app.get("/", summary="Статус системы")
async def root():
    """Базовая проверка работоспособности системы"""
    return {
        "status": "AI Agent Farm is running!",
        "version": "1.0.0-beta",
        "message": "🤖 Мощная многоагентная система для исследований готова к работе",
        "api_docs": "/docs",
        "available_crews": list(CREW_TYPE_INFO.keys())
    }

@app.get("/health", response_model=SystemStatus, summary="Детальный статус системы")
async def health_check():
    """Проверка здоровья всех компонентов системы"""
    
    # Проверка Celery
    try:
        # Ping Celery workers
        active_workers = celery_app.control.inspect().active() or {}
        celery_status = "healthy" if active_workers else "no_workers"
    except Exception:
        celery_status = "unhealthy"
    
    # Проверка Redis (через Celery broker)
    try:
        celery_app.broker_connection().ensure_connection(max_retries=1)
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"
    
    # Подсчет активных задач (упрощенно)
    try:
        inspect = celery_app.control.inspect()
        active_tasks = sum(len(tasks) for tasks in (inspect.active() or {}).values())
    except:
        active_tasks = 0
    
    overall_status = "healthy" if all([
        celery_status != "unhealthy", 
        redis_status != "unhealthy"
    ]) else "unhealthy"
    
    return SystemStatus(
        status=overall_status,
        timestamp=datetime.now(),
        version="1.0.0-beta", 
        components={
            "api": "healthy",
            "celery": celery_status,
            "redis": redis_status,
            "agents": "ready"
        },
        active_tasks=active_tasks,
        completed_tasks=0  # Можно добавить реальную статистику
    )

@app.get("/crews", summary="Информация о типах команд")
async def get_crew_types():
    """Получить информацию о доступных типах команд агентов"""
    return {
        "available_crews": CREW_TYPE_INFO,
        "default": "general",
        "total": len(CREW_TYPE_INFO)
    }

@app.post("/research", response_model=ResearchResponse, summary="Запуск исследования")
async def create_research(request: ResearchRequest):
    """
    Запускает новое исследование с выбранной командой агентов
    
    - **topic**: Тема для исследования (обязательно)
    - **crew_type**: Тип команды агентов (по умолчанию: general)
    - **language**: Язык результата (ru/en, по умолчанию: ru)
    - **depth**: Глубина анализа (basic/standard/comprehensive, по умолчанию: standard)
    """
    
    try:
        # Генерация уникального ID задачи
        task_id = f"research_{uuid.uuid4().hex[:12]}"
        
        logger.info(f"🚀 Создание задачи {task_id}: {request.topic} (команда: {request.crew_type})")
        
        # Запуск асинхронной задачи Celery
        celery_task = research_task.delay(
            topic=request.topic,
            crew_type=request.crew_type,
            language=request.language,
            depth=request.depth
        )
        
        # Получаем информацию о команде
        crew_info = CREW_TYPE_INFO.get(request.crew_type, CREW_TYPE_INFO["general"])
        
        # Оценка времени выполнения
        time_estimates = {
            "basic": "2-5 минут",
            "standard": "5-10 минут", 
            "comprehensive": "10-15 минут"
        }
        
        response = ResearchResponse(
            task_id=celery_task.id,
            status="PENDING",
            message=f"Исследование '{request.topic}' принято в работу командой '{crew_info['name']}'",
            estimated_time=time_estimates.get(request.depth, "5-10 минут"),
            created_at=datetime.now(),
            crew_info=crew_info
        )
        
        logger.info(f"✅ Задача {task_id} создана успешно")
        return response
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания задачи: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка запуска исследования: {str(e)}")

@app.get("/result/{task_id}", response_model=TaskResult, summary="Получение результата")
async def get_result(task_id: str):
    """
    Получает результат исследования по ID задачи
    
    Возможные статусы:
    - **PENDING**: Задача в очереди
    - **PROCESSING**: Агенты работают над исследованием  
    - **SUCCESS**: Исследование завершено успешно
    - **FAILURE**: Произошла ошибка
    """
    
    try:
        # Получение результата из Celery
        celery_result = celery_app.AsyncResult(task_id)
        
        status = celery_result.status
        progress = 0
        result_data = None
        error = None
        processing_time = None
        
        if status == "PENDING":
            progress = 0
        elif status == "PROGRESS":
            # Получаем прогресс из метаданных
            meta = celery_result.info or {}
            progress = meta.get('current', 0)
        elif status == "SUCCESS":
            progress = 100
            result_data = celery_result.result
            processing_time = result_data.get('processing_time') if isinstance(result_data, dict) else None
        elif status == "FAILURE":
            progress = 0
            error = str(celery_result.info)
        
        return TaskResult(
            task_id=task_id,
            status=status,
            progress=progress,
            result=result_data,
            error=error,
            processing_time=processing_time,
            created_at=datetime.now(),  # Можно улучшить, сохраняя реальное время
            completed_at=datetime.now() if status == "SUCCESS" else None
        )
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения результата {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения результата: {str(e)}")

@app.delete("/task/{task_id}", summary="Отмена задачи")
async def cancel_task(task_id: str):
    """Отменяет выполнение задачи (если возможно)"""
    
    try:
        celery_app.control.revoke(task_id, terminate=True)
        logger.info(f"🚫 Задача {task_id} отменена")
        
        return {
            "task_id": task_id,
            "status": "cancelled",
            "message": "Задача отменена"
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка отмены задачи {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка отмены задачи: {str(e)}")

@app.get("/tasks", summary="Список активных задач")
async def list_active_tasks():
    """Получить список всех активных задач"""
    
    try:
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active() or {}
        scheduled_tasks = inspect.scheduled() or {}
        
        return {
            "active_tasks": active_tasks,
            "scheduled_tasks": scheduled_tasks,
            "total_active": sum(len(tasks) for tasks in active_tasks.values()),
            "total_scheduled": sum(len(tasks) for tasks in scheduled_tasks.values())
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения списка задач: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка получения списка задач")

# Обработчики ошибок
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {
        "error": "Not Found",
        "message": "Эндпоинт не найден",
        "available_endpoints": [
            "GET /",
            "GET /health", 
            "GET /crews",
            "POST /research",
            "GET /result/{task_id}",
            "GET /docs"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "error": "Internal Server Error",
        "message": "Внутренняя ошибка сервера. Проверьте логи для деталей.",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
