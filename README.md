# 🌾 AI Farm - Система автоматизированных AI исследований

[![Version](https://img.shields.io/badge/version-1.0.1alpha-red.svg)](https://github.com/your-repo/ai-farm)
[![Python](https://img.shields.io/badge/python-3.11.2+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-28.4.0+-blue.svg)](https://docker.com)
[![Status](https://img.shields.io/badge/status-ready%20for%20testing-green.svg)]()

## 📋 Оглавление

- [Обзор](#обзор)
- [Быстрый старт](#быстрый-старт)
- [Архитектура](#архитектура)
- [Установка и настройка](#установка-и-настройка)
- [API Documentation](#api-documentation)
- [Конфигурация](#конфигурация)
- [Разработка](#разработка)
- [Troubleshooting](#troubleshooting)
- [Безопасность](#безопасность)

## 🎯 Обзор

**AI Farm** - это масштабируемая платформа для автоматизации исследовательских задач с использованием передовых AI технологий. Система разработана для интеграции с workflow-системами (n8n, Zapier) и обеспечивает асинхронное выполнение исследований через REST API.

### ✨ Ключевые возможности

- 🤖 **AI Research Engine** - Автоматизированные исследования через Google Gemini 2.5 Flash
- 🔄 **Асинхронная обработка** - Task queue система на основе Celery + Redis  
- 🌐 **REST API** - Полнофункциональный API для автоматизации
- 🛡️ **VPN интеграция** - Обход геоблокировок через xray-core
- 📊 **Web мониторинг** - Streamlit интерфейс для отслеживания задач
- 🐳 **Docker готовность** - Контейнеризация для легкого развертывания

### 🎯 Текущий статус

✅ **Готово к тестированию** - Система полностью функциональна для базовых исследований  
🔄 **В разработке** - Интеграция с n8n, решение зависимостей CrewAI  
⚠️ **Известные ограничения** - CrewAI временно отключен из-за конфликтов зависимостей

## 🚀 Быстрый старт

### Минимальные требования
```bash
# Системные требования
- Python 3.11.2+
- Docker 28.4.0+ 
- 4GB RAM
- 10GB свободного места

# Активные сервисы
- xray-core (VPN proxy на порту 10809)
- Доступ к Google Gemini API
```

### ⚡ Запуск за 30 секунд

```bash
# 1. Перейти в директорию проекта
cd /home/su/ai-farm

# 2. Запуск через Docker Compose (рекомендуется)
docker compose up -d --build

# 3. Проверка статуса
curl http://localhost:8000/health

# 4. Тестовый запрос
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence", "depth": "basic"}'
```

### 🧪 Альтернативный запуск (для тестирования)

```bash
# Запуск standalone test API
cd /home/su/ai-farm
source test_env/bin/activate
uvicorn test_api:app --host 0.0.0.0 --port 8000

# Тестирование в отдельном терминале
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Blockchain Technology", "depth": "comprehensive"}'
```

## 🏗️ Архитектура

### Компоненты системы

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Celery        │    │   Redis         │
│   (REST API)    │───►│   (Workers)     │───►│   (Broker)      │
│   Port: 8000    │    │   (Tasks)       │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌─────────────────┐              
│   Streamlit     │    │   Google        │              
│   (Monitoring)  │    │   Gemini API    │              
│   Port: 8501    │    │   (via VPN)     │              
└─────────────────┘    └─────────────────┘              
         │                       │                       
         ▼                       ▼                       
┌─────────────────────────────────────────────────────┐
│                xray-core VPN                        │
│            (Port: 10809)                            │
└─────────────────────────────────────────────────────┘
```

### Структура файлов

```
/home/su/ai-farm/
├── 📁 app/                        # Основные модули
│   ├── api_simple.py              # ✅ Упрощенная FastAPI (активная)
│   ├── api.py                     # ⚠️  Полная FastAPI (с CrewAI)
│   ├── tasks.py                   # Celery задачи
│   ├── app.py                     # Streamlit интерфейс
│   └── main_crew.py               # CrewAI агенты (отключены)
├── 📁 test_env/                   # Python виртуальная среда
├── 🔧 .env                        # API ключи (НЕ commit в Git!)
├── 🔧 requirements_minimal.txt    # ✅ Минимальные зависимости
├── 🔧 requirements.txt            # ⚠️  Полные зависимости
├── 🐳 docker-compose.yml          # Docker конфигурация
├── 🐳 Dockerfile                  # Docker образ
├── 📄 main.py                     # Legacy Streamlit app
├── 🧪 test_api.py                 # Standalone тестовая API
├── 📚 documentation.html          # HTML документация
└── 📖 README.md                   # Этот файл
```

## 🔧 Установка и настройка

### 1. Проверка окружения

```bash
# Проверить системные требования
python3 --version    # Должно быть 3.11.2+
docker --version     # Должно быть 28.4.0+

# Проверить VPN прокси
curl -s http://httpbin.org/ip --proxy http://127.0.0.1:10809

# Проверить процессы
ps aux | grep xray   # Должен быть запущен xray-core
```

### 2. Настройка переменных окружения

```bash
# Файл .env уже создан, но можно проверить
cat /home/su/ai-farm/.env

# Структура .env файла:
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 3. Выбор режима запуска

#### Режим A: Docker Compose (Production-ready)

```bash
cd /home/su/ai-farm

# Запуск всех сервисов
docker compose up -d --build

# Проверка статуса
docker compose ps
docker compose logs api -f
```

**Сервисы в Docker Compose:**
- `redis` - Брокер сообщений Redis
- `api` - FastAPI с минимальными зависимостями
- `worker` - Celery worker для обработки задач

#### Режим B: Standalone Test (Быстрое тестирование)

```bash
cd /home/su/ai-farm
source test_env/bin/activate
uvicorn test_api:app --host 0.0.0.0 --port 8000 &
```

#### Режим C: Streamlit мониторинг

```bash
cd /home/su/ai-farm
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
# Открыть http://localhost:8501 в браузере
```

### 4. Проверка установки

```bash
# Проверить API health
curl http://localhost:8000/health

# Создать тестовую задачу
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Research", "description": "Quick test", "depth": "basic"}'

# Проверить результат (замените TASK_ID на полученный ID)
curl http://localhost:8000/result/TASK_ID

# Список всех задач
curl http://localhost:8000/tasks
```

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 🚀 POST /research
Запуск нового исследования

**Request:**
```json
{
  "topic": "Research topic",
  "description": "Optional detailed description",
  "depth": "basic|comprehensive"
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Исследование запущено успешно"
}
```

#### 📊 GET /result/{task_id}
Получение результата и прогресса задачи

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success|pending|started|failure",
  "result": {
    "topic": "Research topic",
    "description": "Description",
    "research_content": "# Detailed research content...",
    "metadata": {
      "model_used": "gemini-2.5-flash",
      "depth": "comprehensive",
      "generated_at": "2025-10-01 06:00:00"
    }
  },
  "error": null,
  "progress": 100
}
```

#### 📋 GET /tasks
Список всех задач

**Response:**
```json
{
  "tasks": [
    {
      "task_id": "uuid",
      "topic": "Topic name",
      "status": "success",
      "progress": 100
    }
  ]
}
```

#### ❤️ GET /health
Проверка состояния системы

**Response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "message": "AI Farm API работает корректно"
}
```

### 📖 Интерактивная документация

```bash
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc

# OpenAPI JSON
http://localhost:8000/openapi.json
```

## ⚙️ Конфигурация

### Порты системы

| Порт  | Сервис         | Описание                    |
|-------|----------------|-----------------------------|
| 10809 | xray-core      | VPN прокси сервер          |
| 8000  | FastAPI        | REST API интерфейс         |
| 8501  | Streamlit      | Веб-интерфейс мониторинга  |
| 6379  | Redis          | Брокер сообщений (Docker)  |

### VPN конфигурация

| Параметр     | Значение                        |
|--------------|--------------------------------|
| Proxy URL    | `http://127.0.0.1:10809`      |
| Docker Proxy | `http://172.17.0.1:10809`     |
| Protocol     | VLESS over WebSocket           |
| External IP  | 89.22.226.247                  |
| Status       | ✅ Активен                      |

### Переменные окружения

```bash
# Основные API ключи
GOOGLE_API_KEY=your_google_api_key    # Google Gemini API
SERPER_API_KEY=your_serper_api_key    # Serper search API (опционально)

# VPN прокси (автоматически в Docker)
HTTP_PROXY=http://172.17.0.1:10809
HTTPS_PROXY=http://172.17.0.1:10809
```

## 👨‍💻 Разработка

### Статус компонентов

| Компонент              | Статус | Описание                           |
|------------------------|--------|------------------------------------|
| ✅ VPN Infrastructure   | Ready  | xray-core с VLESS                  |
| ✅ AI Integration       | Ready  | Google Gemini 2.5 Flash            |
| ✅ Task Queue System    | Ready  | Redis + Celery                     |
| ✅ REST API            | Ready  | FastAPI с полным набором endpoints |
| ✅ Docker Support       | Ready  | docker-compose для развертывания    |
| ✅ Test Framework       | Ready  | Standalone тестовая API            |
| 🔄 n8n Integration     | Pending| Готовность к интеграции с n8n      |
| ⚠️ CrewAI Integration   | Issues | Конфликты зависимостей             |

### Известные проблемы

1. **CrewAI Dependencies** - Конфликт версий chromadb/typer
   ```bash
   # Временное решение: использовать requirements_minimal.txt
   cp requirements_minimal.txt requirements.txt
   ```

2. **Docker Build Time** - Долгая сборка при полных зависимостях
   ```bash
   # Решение: используется runtime установка в docker-compose.yml
   command: sh -c "cp requirements_minimal.txt requirements.txt && pip install -r requirements.txt && ..."
   ```

3. **docker-compose.yml version** - Устаревший атрибут version
   ```bash
   # TODO: удалить строку 'version: 3.8' из docker-compose.yml
   ```

### Мониторинг и отладка

```bash
# Просмотр логов Docker сервисов
docker compose logs api -f      # FastAPI логи
docker compose logs worker -f   # Celery worker логи
docker compose logs redis -f    # Redis логи

# Системные логи
journalctl -u xray -f          # xray VPN логи

# Проверка состояния
docker compose ps              # Статус контейнеров
curl http://localhost:8000/health  # API health check
curl http://localhost:8000/tasks   # Активные задачи
```

### Тестирование

```bash
# Быстрый функциональный тест
cd /home/su/ai-farm
source test_env/bin/activate

# Запуск test API
uvicorn test_api:app --host 0.0.0.0 --port 8000 &

# Создание тестовой задачи
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI Testing", "depth": "basic"}')

echo $TASK_RESPONSE

# Получение task_id и проверка результата
TASK_ID=$(echo $TASK_RESPONSE | grep -o '"task_id":"[^"]*' | grep -o '[^"]*$')
sleep 10  # Ждем выполнения
curl http://localhost:8000/result/$TASK_ID
```

## 🔧 Troubleshooting

### Проблема: API не запускается

```bash
# Проверить занятость порта
netstat -tlnp | grep :8000
# или
ss -tlnp | grep :8000

# Проверить Docker сервисы
docker compose ps
docker compose logs api
```

### Проблема: VPN не работает

```bash
# Проверить xray процесс
ps aux | grep xray

# Проверить доступность прокси
curl -s --max-time 5 http://httpbin.org/ip --proxy http://127.0.0.1:10809

# Перезапустить xray (если есть права)
# sudo systemctl restart xray
```

### Проблема: Задачи не выполняются

```bash
# Проверить Redis подключение
docker exec -it ai-farm-redis-1 redis-cli ping

# Проверить Celery worker
docker compose logs worker -f

# Проверить очередь задач
curl http://localhost:8000/tasks
```

### Проблема: Ошибки зависимостей

```bash
# Использовать минимальные зависимости
cd /home/su/ai-farm
cp requirements_minimal.txt requirements.txt

# Пересобрать контейнеры
docker compose down
docker compose up -d --build
```

## 🔐 Безопасность

### Управление секретами

- 🔑 **API ключи** хранятся в `.env` файле (НЕ commit в Git!)
- 🌐 **VPN конфигурация** в `/usr/local/etc/xray/config.json`
- 📦 **Redis** без аутентификации (только localhost/container network)

### Сетевая безопасность

- 🏠 Все сервисы привязаны к localhost или Docker networks
- 🛡️ VPN трафик маршрутизируется через проверенные серверы
- 🐳 Docker networks изолированы от внешнего доступа

### Рекомендации для production

```bash
# 1. Настроить аутентификацию Redis
# Добавить в docker-compose.yml:
# redis:
#   command: redis-server --requirepass your_password

# 2. Добавить HTTPS для FastAPI
# uvicorn app.api_simple:app --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem

# 3. Настроить firewall
# ufw allow 8000/tcp
# ufw deny 6379/tcp

# 4. Регулярные обновления
# docker compose pull
# pip install -r requirements.txt --upgrade
```

## 🤝 Интеграция с n8n

Система готова для интеграции с n8n workflow автоматизацией:

### Настройка webhook в n8n

1. **Создание задачи**
   - URL: `http://your-server:8000/research`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: `{"topic": "{{$json.topic}}", "depth": "comprehensive"}`

2. **Polling результата**
   - URL: `http://your-server:8000/result/{{$json.task_id}}`
   - Method: GET
   - Interval: 30 seconds
   - Stop condition: `status === "success" || status === "failure"`

3. **Обработка результатов**
   - Parse: `result.research_content`
   - Metadata: `result.metadata`

## 📞 Поддержка

### Для следующего агента

```bash
# Текущий статус системы
Location: /home/su/ai-farm
Version: v1.0.1alpha
Status: ✅ Ready for testing and n8n integration
Environment: Debian GNU/Linux, Python 3.11.2, Docker 28.4.0

# Быстрый тест работоспособности
cd /home/su/ai-farm && curl http://localhost:8000/health

# Критические файлы
- .env (API keys - НЕ изменять)
- docker-compose.yml (основная конфигурация)
- app/api_simple.py (активная FastAPI)
- requirements_minimal.txt (рабочие зависимости)
```

### Следующие шаги для развития

1. **Немедленные задачи**
   - Решить конфликты зависимостей CrewAI
   - Удалить устаревший `version` из docker-compose.yml
   - Настроить production-ready Redis с аутентификацией

2. **Интеграция**
   - Тестирование интеграции с n8n
   - Добавление webhook endpoints
   - Улучшение error handling

3. **Масштабирование**
   - Горизонтальное масштабирование Celery workers
   - Monitoring и alerting
   - Backup и recovery процедуры

---

**© 2025 AI Farm System - v1.0.1alpha**  
*Готов к тестированию и интеграции с workflow системами*
