from app.tasks import run_research_crew
import time
import redis
import json

print("🧪 Тестирование системы мониторинга...")

# Подключаемся к Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Запускаем тестовую задачу
topic = "Блокчейн технологии в логистике"
print(f"📋 Запуск исследования: '{topic}'")

task = run_research_crew.delay(topic)
task_id = task.id
print(f"🆔 ID задачи: {task_id}")

# Мониторим выполнение
print("🔄 Мониторинг выполнения задачи...")
for i in range(20):  # Максимум 60 секунд мониторинга
    try:
        # Проверяем основной статус Celery
        task_info = redis_client.get(f"celery-task-meta-{task_id}")
        
        # Проверяем дополнительный статус
        status_info = redis_client.get(f"task-status-{task_id}")
        
        if task_info:
            task_data = json.loads(task_info)
            status = task_data.get('status', 'UNKNOWN')
            
            print(f"⏱️  [{i*3}s] Статус: {status}")
            
            if status_info:
                status_data = json.loads(status_info)
                message = status_data.get('message', '')
                progress = status_data.get('progress', 0)
                print(f"    📊 Прогресс: {progress}% - {message}")
            
            if status == 'SUCCESS':
                print("✅ Задача завершена успешно!")
                result = task_data.get('result', '')
                print(f"📄 Длина результата: {len(result)} символов")
                break
            elif status == 'FAILURE':
                print("❌ Задача завершилась с ошибкой!")
                break
                
        time.sleep(3)
        
    except Exception as e:
        print(f"⚠️  Ошибка мониторинга: {e}")
        time.sleep(3)

print("🏁 Тест мониторинга завершен!")
