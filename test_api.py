"""
Тестовая версия FastAPI для проверки концепции
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import uuid
import time
from datetime import datetime

app = FastAPI(title="AI Farm Test API", description="Тестовая версия API")

# Симуляция хранилища задач
tasks_storage = {}

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

def simulate_research(topic: str, description: str = "", depth: str = "comprehensive"):
    """Симуляция исследовательского процесса"""
    return {
        "topic": topic,
        "description": description,
        "research_content": f"""
# Исследование по теме: {topic}

## Введение
Данное исследование посвящено анализу темы "{topic}".

## Основной анализ
{description if description else "Детальный анализ темы с учетом современных тенденций и подходов."}

Глубина анализа: {depth}

## Ключевые выводы
1. Тема является актуальной и требует дальнейшего изучения
2. Существуют различные подходы к решению связанных вопросов
3. Необходимы дополнительные исследования для полного понимания

## Рекомендации
1. Провести дополнительный анализ
2. Изучить международный опыт
3. Разработать практические рекомендации

## Источники
- Научная литература по теме
- Экспертные мнения
- Актуальные исследования
        """.strip(),
        "metadata": {
            "model_used": "gemini-2.5-flash (simulated)",
            "depth": depth,
            "generated_at": str(datetime.now())
        }
    }

@app.post("/research", response_model=TaskResponse)
async def start_research(request: ResearchRequest):
    """Запускает новое исследование"""
    try:
        task_id = str(uuid.uuid4())
        
        # Сохраняем задачу
        tasks_storage[task_id] = {
            "status": "pending",
            "topic": request.topic,
            "description": request.description,
            "depth": request.depth,
            "progress": 0,
            "message": "Задача поставлена в очередь",
            "created_at": datetime.now()
        }
        
        return TaskResponse(
            task_id=task_id,
            status="pending", 
            message="Исследование запущено успешно"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запуска задачи: {str(e)}")

@app.get("/result/{task_id}", response_model=TaskResult)
async def get_result(task_id: str):
    """Получает результат исследования по ID задачи"""
    try:
        if task_id not in tasks_storage:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        task = tasks_storage[task_id]
        
        # Симуляция прогресса задачи
        if task["status"] == "pending":
            task["status"] = "started"
            task["progress"] = 10
            task["message"] = "Начинаем исследование..."
            
        elif task["status"] == "started":
            # Симулируем выполнение через 5 секунд
            time_passed = (datetime.now() - task["created_at"]).seconds
            
            if time_passed < 3:
                task["progress"] = 30
                task["message"] = "Анализируем тему..."
            elif time_passed < 6:
                task["progress"] = 70
                task["message"] = "Генерируем результаты..."
            else:
                # Завершаем задачу
                task["status"] = "success"
                task["progress"] = 100
                task["message"] = "Исследование завершено успешно"
                task["result"] = simulate_research(
                    task["topic"], 
                    task["description"] or "", 
                    task["depth"]
                )
        
        return TaskResult(
            task_id=task_id,
            status=task["status"],
            result=task.get("result"),
            error=task.get("error"),
            progress=task["progress"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения результата: {str(e)}")

@app.get("/tasks")
async def list_tasks():
    """Возвращает список всех задач"""
    try:
        tasks = []
        for task_id, task_data in tasks_storage.items():
            tasks.append({
                "task_id": task_id,
                "topic": task_data["topic"],
                "status": task_data["status"],
                "progress": task_data["progress"]
            })
        
        return {"tasks": tasks}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка задач: {str(e)}")

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {
        "status": "healthy",
        "message": "AI Farm Test API работает корректно",
        "tasks_count": len(tasks_storage)
    }

@app.get("/")
async def root():
    """Корневая страница с информацией об API"""
    return {
        "message": "AI Farm Test API",
        "version": "1.0.0",
        "endpoints": [
            "POST /research - Запустить исследование", 
            "GET /result/{task_id} - Получить результат",
            "GET /tasks - Список всех задач",
            "GET /health - Проверка состояния"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
