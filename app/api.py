from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from celery.result import AsyncResult
from app.tasks import celery_app
import redis
import json
from datetime import datetime
from typing import Optional

# Подключение к Redis для дополнительного статуса
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Модели данных для API
class ResearchRequest(BaseModel):
    topic: str = Field(..., description="Тема для исследования", example="Блокчейн в логистике")
    
class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class ResultResponse(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None
    message: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

# Создание FastAPI приложения
app = FastAPI(
    title="🤖 AI Agent Farm API",
    description="""
    **Мощный API для запуска исследовательских задач с помощью команды CrewAI агентов.**
    
    ## Возможности:
    - 🚀 **Асинхронный запуск исследований** через Celery
    - 🔍 **Детальное отслеживание прогресса** в реальном времени  
    - 🤖 **Команда ИИ-агентов** с Gemini 2.5 Flash
    - 🌐 **VPN интеграция** для доступа к заблокированным ресурсам
    - 📊 **Структурированные отчёты** с анализом и источниками
    
    ## Workflow:
    1. POST `/research` - Запустить исследование
    2. GET `/result/{task_id}` - Проверить статус и получить результат
    """,
    version="1.0.0",
    contact={
        "name": "AI Farm Support",
        "email": "admin@ai-farm.local"
    }
)

@app.get("/")
async def root():
    """
    Главная страница API - информация о статусе системы
    """
    try:
        # Проверяем подключение к Redis
        redis_status = "🟢 Подключен" if redis_client.ping() else "🔴 Не подключен"
        
        # Проверяем статус Celery
        celery_inspect = celery_app.control.inspect()
        active_tasks = celery_inspect.active()
        celery_status = "🟢 Активен" if active_tasks is not None else "🔴 Недоступен"
        
        return {
            "service": "🤖 AI Agent Farm API",
            "version": "1.0.0",
            "status": "🚀 Работает",
            "components": {
                "redis": redis_status,
                "celery": celery_status,
                "api": "🟢 Активен"
            },
            "endpoints": {
                "start_research": "POST /research",
                "get_result": "GET /result/{task_id}",
                "docs": "GET /docs"
            }
        }
    except Exception as e:
        return {
            "service": "🤖 AI Agent Farm API",
            "status": "⚠️ Частичные проблемы", 
            "error": str(e)
        }

@app.post("/research", response_model=TaskResponse, tags=["Research"])
async def start_research(request: ResearchRequest):
    """
    🚀 **Запуск нового исследования**
    
    Отправляет задачу в очередь Celery и немедленно возвращает ID задачи.
    ИИ-агенты начнут работу в фоновом режиме.
    
    **Параметры:**
    - topic: Тема для глубокого исследования
    
    **Возвращает:**
    - task_id: Уникальный идентификатор задачи
    - status: Текущий статус (PENDING)
    - message: Сообщение о принятии задачи
    """
    try:
        # Импортируем задачу здесь, чтобы избежать циклических импортов
        from app.tasks import run_research_crew
        
        # Запускаем задачу в Celery
        task = run_research_crew.delay(request.topic)
        
        return TaskResponse(
            task_id=task.id,
            status="PENDING", 
            message=f"Исследование темы '{request.topic}' принято в работу. Используйте task_id для отслеживания прогресса."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка при запуске исследования: {str(e)}"
        )

@app.get("/result/{task_id}", response_model=ResultResponse, tags=["Research"])
async def get_research_result(task_id: str):
    """
    📊 **Получение результата исследования**
    
    Проверяет статус задачи и возвращает результат, если он готов.
    Используйте этот эндпоинт для периодической проверки готовности.
    
    **Параметры:**
    - task_id: ID задачи, полученный при запуске
    
    **Возвращает:**
    - task_id: ID задачи
    - status: PENDING | PROGRESS | SUCCESS | FAILURE
    - progress: Процент выполнения (0-100)
    - message: Описание текущего этапа
    - result: Готовый отчёт (только при SUCCESS)
    - error: Описание ошибки (только при FAILURE)
    """
    try:
        # Получаем основную информацию о задаче из Celery
        task_result = AsyncResult(task_id, app=celery_app)
        
        # Получаем дополнительный статус из Redis
        status_info = None
        try:
            status_data = redis_client.get(f"task-status-{task_id}")
            if status_data:
                status_info = json.loads(status_data)
        except:
            pass
        
        if task_result.ready():
            # Задача завершена
            if task_result.successful():
                # ИСПРАВЛЕНИЕ: Правильно получаем результат
                result = task_result.result
                if isinstance(result, str):
                    # Результат уже строка - используем как есть
                    final_result = result
                else:
                    # Если результат не строка, преобразуем в JSON
                    final_result = json.dumps(result, ensure_ascii=False, indent=2)
                
                return ResultResponse(
                    task_id=task_id,
                    status="SUCCESS",
                    progress=100,
                    message="Исследование завершено успешно!",
                    result=final_result
                )
            else:
                # Произошла ошибка
                error_info = "Неизвестная ошибка"
                if hasattr(task_result, 'info') and task_result.info:
                    if isinstance(task_result.info, dict):
                        error_info = task_result.info.get('error', str(task_result.info))
                    else:
                        error_info = str(task_result.info)
                
                return ResultResponse(
                    task_id=task_id,
                    status="FAILURE", 
                    progress=0,
                    message="Задача завершилась с ошибкой",
                    error=error_info
                )
        else:
            # Задача ещё выполняется
            progress = 0
            message = "Задача в очереди, ожидание обработки..."
            
            # Используем дополнительную информацию из Redis, если есть
            if status_info:
                progress = status_info.get('progress', 0)
                message = status_info.get('message', message)
                
            # Или информацию из meta Celery
            elif hasattr(task_result, 'info') and isinstance(task_result.info, dict):
                progress = task_result.info.get('current', 0)
                message = task_result.info.get('status', message)
            
            return ResultResponse(
                task_id=task_id,
                status="PROGRESS" if progress > 0 else "PENDING",
                progress=progress,
                message=message
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении результата: {str(e)}"
        )

@app.get("/status", tags=["System"])
async def get_system_status():
    """
    📊 **Статус системы**
    
    Возвращает общую информацию о состоянии всех компонентов системы.
    """
    try:
        # Статус Redis
        redis_status = "connected" if redis_client.ping() else "disconnected"
        
        # Количество задач в очереди
        queue_length = redis_client.llen('celery') if redis_status == "connected" else 0
        
        # Статус Celery воркеров
        celery_inspect = celery_app.control.inspect()
        active_tasks = celery_inspect.active()
        registered_tasks = celery_inspect.registered()
        
        celery_workers = 0
        if active_tasks:
            celery_workers = len(active_tasks.keys())
            
        return {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "api": "running",
                "redis": redis_status,
                "celery_workers": celery_workers
            },
            "queue": {
                "pending_tasks": queue_length
            },
            "info": {
                "total_endpoints": len(app.routes),
                "api_version": "1.0.0"
            }
        }
        
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "system": "error",
            "error": str(e)
        }

# Добавляем CORS headers для работы с n8n и другими клиентами
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
