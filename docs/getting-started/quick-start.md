# 🚀 Быстрый старт

Добро пожаловать в AI Agent Farm! Этот гид поможет вам запустить систему за несколько минут.

## Предварительные требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- API ключи: Gemini API, Serper API

## Вариант 1: Docker (Рекомендуется)

### 1. Клонирование репозитория
```bash
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
```

### 2. Настройка переменных окружения
```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```env
GOOGLE_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
DEBUG=false
LANGUAGE=ru
```

### 3. Запуск системы
```bash
docker compose up -d
```

### 4. Проверка работы
```bash
curl http://localhost:8000/
```

## Первое исследование

Создайте ваше первое исследование:

```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Искусственный интеллект в образовании"}'
```

Получите результат:
```bash
curl "http://localhost:8000/result/{task_id}"
```

🎉 **Поздравляем! AI Agent Farm запущен и готов к работе!**
