"""
Упрощенный FastAPI модуль для AI фермы без CrewAI зависимостей
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import celery
import redis
import json
import uuid
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Настройка Redis и Celery
redis_client = redis.Redis(host='redis', port=6379, db=0)
app = FastAPI(title="AI Farm API", description="API для управления AI исследованиями")

# Celery app
celery_app = celery.Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

class ResearchRequest(BaseModel):
    topic: str
    description: Optional[str] = None
    depth: Optional[str] = "comprehensive"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: Optional[str] = None

class TaskResult(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[int] = None

@celery_app.task(bind=True)
def simple_research_task(self, topic: str, description: str = "", depth: str = "comprehensive"):
    """Упрощенная исследовательская задача с Gemini"""
    task_id = self.request.id
    
    try:
        # Обновляем статус: начали
        redis_client.hset(
            f"task:{task_id}", 
            mapping={
                "status": "started",
                "progress": 10,
                "message": f"Начинаем исследование по теме: {topic}"
            }
        )
        
        # Подготавливаем запрос к Gemini
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Создаем промпт
        prompt = f"""
Выполни подробное исследование по теме: "{topic}"

Описание: {description if description else "Не указано"}
Глубина анализа: {depth}

Структурируй ответ следующим образом:
1. **Введение** - краткий обзор темы
2. **Основной анализ** - детальное исследование
3. **Ключевые выводы** - главные результаты
4. **Рекомендации** - практические предложения
5. **Источники** - релевантные ресурсы для изучения

Используй актуальную информацию и предоставь всестороннее исследование.
"""
        
        # Обновляем прогресс
        redis_client.hset(
            f"task:{task_id}", 
            mapping={
                "status": "processing",
                "progress": 30,
                "message": "Отправляем запрос к Gemini AI..."
            }
        )
        
        # Генерируем ответ
        response = model.generate_content(prompt)
        
        redis_client.hset(
            f"task:{task_id}", 
            mapping={
                "status": "processing", 
                "progress": 80,
                "message": "Обрабатываем результаты исследования..."
            }
        )
        
        # Формируем результат
        result = {
            "topic": topic,
            "description": description,
            "research_content": response.text,
            "metadata": {
                "model_used": "gemini-2.5-flash",
                "depth": depth,
                "generated_at": str(__import__('datetime').datetime.now())
            }
        }
        
        # Сохраняем результат
        redis_client.hset(
            f"task:{task_id}", 
            mapping={
                "status": "success",
                "progress": 100,
                "result": json.dumps(result, ensure_ascii=False),
                "message": "Исследование завершено успешно"
            }
        )
        
        return result
        
    except Exception as e:
        redis_client.hset(
            f"task:{task_id}", 
            mapping={
                "status": "failure",
                "progress": 0,
                "error": str(e),
                "message": f"Ошибка при выполнении исследования: {str(e)}"
            }
        )
        raise e

@app.post("/research", response_model=TaskResponse)
async def start_research(request: ResearchRequest):
    """Запускает новое исследование"""
    try:
        # Запускаем задачу
        task = simple_research_task.delay(
            topic=request.topic,
            description=request.description or "",
            depth=request.depth
        )
        
        # Сохраняем начальную информацию о задаче
        redis_client.hset(
            f"task:{task.id}",
            mapping={
                "status": "pending",
                "topic": request.topic,
                "progress": 0,
                "message": "Задача поставлена в очередь"
            }
        )
        
        return TaskResponse(
            task_id=task.id,
            status="pending", 
            message="Исследование запущено успешно"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запуска задачи: {str(e)}")

@app.get("/result/{task_id}", response_model=TaskResult)
async def get_result(task_id: str):
    """Получает результат исследования по ID задачи"""
    try:
        # Получаем данные из Redis
        task_data = redis_client.hgetall(f"task:{task_id}")
        
        if not task_data:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        # Декодируем данные
        status = task_data.get(b'status', b'').decode('utf-8')
        progress = int(task_data.get(b'progress', b'0').decode('utf-8'))
        message = task_data.get(b'message', b'').decode('utf-8')
        error = task_data.get(b'error', b'').decode('utf-8') if b'error' in task_data else None
        
        result = None
        if status == "success" and b'result' in task_data:
            try:
                result = json.loads(task_data[b'result'].decode('utf-8'))
            except:
                result = {"content": task_data[b'result'].decode('utf-8')}
        
        return TaskResult(
            task_id=task_id,
            status=status,
            result=result,
            error=error,
            progress=progress
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения результата: {str(e)}")

@app.get("/tasks")
async def list_tasks():
    """Возвращает список всех задач"""
    try:
        task_keys = redis_client.keys("task:*")
        tasks = []
        
        for key in task_keys:
            task_id = key.decode('utf-8').split(':')[1]
            task_data = redis_client.hgetall(key)
            
            tasks.append({
                "task_id": task_id,
                "topic": task_data.get(b'topic', b'').decode('utf-8'),
                "status": task_data.get(b'status', b'').decode('utf-8'),
                "progress": int(task_data.get(b'progress', b'0').decode('utf-8'))
            })
        
        return {"tasks": tasks}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка задач: {str(e)}")

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    try:
        # Проверяем подключение к Redis
        redis_client.ping()
        
        return {
            "status": "healthy",
            "redis": "connected",
            "message": "AI Farm API работает корректно"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "redis": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
