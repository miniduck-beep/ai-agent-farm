# ⚙️ Конфигурация

Подробное описание всех параметров конфигурации AI Agent Farm.

## Переменные окружения

### Основные настройки
```env
# AI API ключи
GOOGLE_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_search_key
OPENAI_API_KEY=your_openai_key  # Опционально

# Системные настройки
DEBUG=false
LOG_LEVEL=INFO
LANGUAGE=ru  # ru или en

# Настройки сервера
HOST=0.0.0.0
PORT=8000

# Redis настройки
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### VPN настройки (опционально)
```env
USE_VPN=false
VPN_SERVER=your_vpn_server
VPN_PORT=10809
VPN_USERNAME=username
VPN_PASSWORD=password
```

### Celery настройки
```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
```

## Docker Compose конфигурации

### Стандартная конфигурация
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
      - celery-worker

  celery-worker:
    build: .
    command: celery -A app.tasks worker --loglevel=info

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### VPN конфигурация
```yaml
# docker-compose.vpn.yml
services:
  xray:
    image: teddysun/xray:latest
    ports:
      - "10809:10809"
    volumes:
      - ./xray-config.json:/etc/xray/config.json

  api:
    environment:
      - https_proxy=http://xray:10809
      - http_proxy=http://xray:10809
```

## Конфигурация агентов

### Настройка LLM модели
```python
# app/config.py
LLM_CONFIG = {
    "model": "gemini-pro",
    "temperature": 0.1,
    "max_tokens": 4000,
    "timeout": 60
}
```

### Типы команд агентов
```python
AGENT_TEAMS = {
    "general": GeneralTeam,
    "business_analyst": BusinessAnalystTeam,
    "content_marketing": ContentMarketingTeam,
    "tech_research": TechResearchTeam,
    "financial_analysis": FinancialAnalysisTeam,
    "startup_consultant": StartupConsultantTeam
}
```

## Настройка логирования

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'ai_agent_farm.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## Настройка безопасности

### API Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/research")
@limiter.limit("5/minute")
async def create_research(request: Request, ...):
    ...
```

### CORS настройки
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Мониторинг и метрики

### Prometheus метрики
```env
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Healthcheck endpoints
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "redis": await check_redis(),
        "celery": await check_celery()
    }
```

## Production настройки

### Использование Gunicorn
```bash
gunicorn app.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Nginx конфигурация
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Рекомендации по безопасности

1. **Не храните API ключи в коде**
2. **Используйте HTTPS в production**
3. **Настройте rate limiting**
4. **Регулярно обновляйте зависимости**
5. **Мониторьте использование API ключей**

## Следующие шаги

После конфигурации:
1. [Запустите быстрый старт](quick-start.md)
2. [Настройте мониторинг](../guides/monitoring.md)
3. [Интегрируйтесь с внешними системами](../guides/integrations.md)
