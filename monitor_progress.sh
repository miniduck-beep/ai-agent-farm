#!/bin/bash
echo "🔄 Мониторинг работы ИИ-агентов..."
echo "Нажмите Ctrl+C для выхода"
echo "=" * 60

while true; do
    echo -e "\n⏰ $(date '+%H:%M:%S') - Проверка активности..."
    
    # Проверим количество задач в очереди Redis
    TASKS_IN_QUEUE=$(docker exec ai-farm-redis-1 redis-cli llen celery 2>/dev/null || echo "0")
    echo "📋 Задач в очереди: $TASKS_IN_QUEUE"
    
    # Проверим статус worker'а
    WORKER_STATUS=$(docker compose ps worker --format "table {{.Status}}" | tail -n 1)
    echo "⚡ Статус worker: $WORKER_STATUS"
    
    # Покажем последние логи worker'а
    echo "📝 Последние логи worker'а:"
    docker compose logs --tail=3 worker 2>/dev/null | tail -n 3 || echo "Логи недоступны"
    
    echo "─────────────────────────────────────────"
    sleep 10
done
