# 🤖 AI Agent Farm - Интеллектуальная Ферма AI Агентов

> **Полностью готовое к продакшену решение для автоматизированных исследований с использованием мульти-агентных систем CrewAI**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-latest-purple.svg)](https://github.com/joaomdmoura/crewAI)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow.svg)](https://pytest.org/)

## 🌟 Ключевые возможности

### 🧠 Интеллектуальное ядро
- **5 специализированных команд агентов** для разных типов исследований
- **Динамическая фабрика команд** с адаптацией под задачи
- **Мульти-языковая поддержка** (русский/английский)
- **Настраиваемая глубина анализа** (базовый/стандартный/исчерпывающий)

### 🔗 Интеграция и интерфейсы
- **REST API** с полной OpenAPI документацией
- **Веб-интерфейс Streamlit** для пользователей
- **Готовый n8n воркфлоу** для автоматизации
- **Асинхронная обработка** с Celery и Redis

### 🛡️ Производственная готовность
- **Comprehensive тестирование** (Unit/Integration/E2E)
- **Docker контейнеризация** с docker-compose
- **Мониторинг здоровья системы** и логирование
- **Graceful обработка ошибок** и retry логика

## 🚀 Быстрый старт

### Запуск полной системы
```bash
# Клонируем репозиторий
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm

# Настраиваем переменные окружения
cp .env.example .env
# Отредактируйте .env с вашими API ключами

# Запускаем всю инфраструктуру
docker compose up -d

# Проверяем статус
curl http://localhost:8000/health
```

### Веб-интерфейс
```bash
# Альтернативный запуск только веб-интерфейса
python run_web_interface.py
# Откройте: http://localhost:8501
```

## 🏗️ Архитектура системы

```
AI Agent Farm
├── 🧠 Core Intelligence
│   ├── CrewFactory - Фабрика команд агентов
│   ├── 5 специализированных команд
│   └── Динамическая генерация задач
├── 🔌 API Layer
│   ├── FastAPI REST endpoints
│   ├── Pydantic модели
│   └── Асинхронная обработка
├── 🌐 User Interfaces
│   ├── Streamlit Web UI
│   ├── OpenAPI документация
│   └── n8n integration
└── 🧪 Quality Assurance
    ├── Pytest тестирование
    ├── Coverage отчеты
    └── CI/CD workflows
```

## 🎯 Специализированные команды агентов

### 1. 🔍 **General Research** (general)
**Агенты:** Исследователь + Аналитический писатель  
**Назначение:** Универсальные исследования любых тем  
**Применение:** Общие вопросы, обзоры, базовый анализ

### 2. 💼 **Business Analysis** (business_analysis)  
**Агенты:** Бизнес-аналитик + Финансовый эксперт + Стратегический консультант  
**Назначение:** Комплексный анализ рынков и бизнес-возможностей  
**Применение:** Анализ конкурентов, оценка рынков, бизнес-планирование

### 3. 📝 **SEO Content** (seo_content)
**Агенты:** SEO исследователь + Контент-писатель + SEO оптимизатор  
**Назначение:** Создание SEO-оптимизированного контента  
**Применение:** Блог-посты, статьи, контент-маркетинг

### 4. 🔬 **Technical Research** (tech_research)
**Агенты:** Технический исследователь + Аналитик архитектуры + Документировщик  
**Назначение:** Глубокий технический анализ  
**Применение:** Обзор технологий, архитектурные решения, техническая документация

### 5. 💰 **Financial Analysis** (financial_analysis)
**Агенты:** Финансовый аналитик + Инвестиционный консультант + Риск-менеджер  
**Назначение:** Финансовые исследования и инвестиционный анализ  
**Применение:** Анализ активов, инвестиционные стратегии, оценка рисков

## 📡 API Endpoints

### Основные endpoints
| Method | Endpoint | Описание |
|--------|----------|----------|
| `GET` | `/` | Информация о системе |
| `POST` | `/research` | Создание исследования |
| `GET` | `/result/{task_id}` | Получение результата |
| `GET` | `/health` | Статус системы |
| `GET` | `/crews` | Доступные команды |
| `GET` | `/tasks` | Активные задачи |
| `DELETE` | `/task/{task_id}` | Отмена задачи |

### Пример запроса исследования
```python
import requests

response = requests.post('http://localhost:8000/research', json={
    "topic": "Анализ рынка искусственного интеллекта в 2024 году",
    "crew_type": "business_analysis",
    "language": "ru",
    "depth": "comprehensive"
})

task_id = response.json()["task_id"]
print(f"Исследование запущено: {task_id}")
```

## 🔗 Интеграция с n8n

### Быстрая настройка
1. **Импорт воркфлоу:** `integrations/n8n/ai-agent-farm-workflow.json`
2. **Настройка URL:** Укажите `http://localhost:8000` 
3. **API ключи:** Настройте аутентификацию
4. **Тестирование:** Запустите тестовое исследование

### Возможности n8n воркфлоу
- ✅ Автоматический запуск исследований через webhook
- ✅ Опрос статуса выполнения с интервалами
- ✅ Форматирование результатов
- ✅ Отправка уведомлений (email, Slack, Telegram)
- ✅ Интеграция с базами данных
- ✅ Кастомизация под ваши процессы

Подробнее: [Руководство по интеграции с n8n](integrations/n8n/README.md)

## 🌐 Веб-интерфейс Streamlit

Интуитивный веб-интерфейс для взаимодействия с системой:

### Основные функции
- 📝 **Форма создания исследования** с валидацией
- 🎯 **Выбор типа команды** из доступных вариантов
- 🌍 **Настройка языка и глубины** анализа
- ⏱️ **Real-time отслеживание статуса** выполнения
- 📊 **Отображение результатов** в удобном формате
- 📋 **История исследований** с возможностью экспорта

### Запуск
```bash
python run_web_interface.py
# Открыть: http://localhost:8501
```

## 🧪 Тестирование

Система включает comprehensive фреймворк тестирования:

### Типы тестов
```bash
make test           # Все тесты
make test-unit      # Unit тесты (быстрые)
make test-integration  # Интеграционные тесты
make test-e2e       # End-to-end тесты
make test-coverage  # С отчетом покрытия
```

### Структура тестов
- **Unit тесты:** API endpoints, валидация, обработка ошибок
- **Integration тесты:** Фабрика команд, генерация задач
- **E2E тесты:** Полный workflow от создания до получения результата

### Покрытие кода
- HTML отчеты в `htmlcov/`
- Minimum coverage threshold: 80%
- Автоматическое тестирование в CI/CD

Подробнее: [Документация по тестированию](docs/testing.md)

## 🛠️ Конфигурация

### Переменные окружения
```bash
# API Keys (обязательные)
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# Redis (опционально)
REDIS_URL=redis://localhost:6379/0

# Настройки (опционально)
DEBUG=false
LOG_LEVEL=INFO
MAX_WORKERS=4
```

### Настройка команд агентов
Кастомизация доступна в `app/main_crew.py`:
- Роли и цели агентов
- Инструменты и capabilities
- Параметры выполнения
- Шаблоны задач

## 📋 Структура проекта

```
ai-agent-farm/
├── 📁 app/                    # Основной код приложения
│   ├── api.py                 # FastAPI endpoints
│   ├── main_crew.py           # Фабрика команд агентов
│   ├── tasks.py               # Celery задачи
│   ├── config.py              # Конфигурация
│   └── web_interface.py       # Streamlit интерфейс
├── 📁 tests/                  # Тестирование
│   ├── unit/                  # Unit тесты
│   ├── integration/           # Integration тесты
│   ├── e2e/                   # End-to-end тесты
│   └── conftest.py            # Настройки pytest
├── 📁 integrations/n8n/       # n8n интеграция
├── 📁 docs/                   # Документация
├── 📁 .github/                # GitHub workflows
├── docker-compose.yml         # Docker конфигурация
├── docker-compose.prod.yml    # Production конфигурация
├── Makefile                   # Команды разработки
└── requirements.txt           # Зависимости
```

## 🚀 Продакшн развертывание

### Docker Compose (рекомендуется)
```bash
# Продакшн конфигурация
docker compose -f docker-compose.prod.yml up -d

# Масштабирование
docker compose up --scale worker=3

# Мониторинг
docker compose logs -f
```

### Мониторинг и метрики
- Health checks: `GET /health`
- Celery monitoring: Flower UI
- Логирование: Structured JSON logs
- Metrics: Custom FastAPI middleware

## 🤝 Участие в разработке

### Настройка dev окружения
```bash
# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Запуск тестов
make test

# Проверка качества кода
make quality
```

### Contribution Guidelines
1. Fork репозиторий
2. Создайте feature branch
3. Добавьте тесты для новой функциональности
4. Убедитесь что все тесты проходят
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE) файл

## 🆘 Поддержка

- **Issues:** [GitHub Issues](https://github.com/miniduck-beep/ai-agent-farm/issues)
- **Discussions:** [GitHub Discussions](https://github.com/miniduck-beep/ai-agent-farm/discussions)
- **Documentation:** [Полная документация](docs/)

---

## 🔧 Дополнительные возможности

### Интеграция с внешними системами
- **Webhook endpoints** для интеграции
- **REST API** для внешних приложений
- **Batch processing** для массовых исследований
- **Export функции** (PDF, DOCX, JSON)

### Расширение функциональности
- **Custom crew types** - добавление новых типов команд
- **Agent personalities** - настройка личности агентов  
- **Knowledge bases** - интеграция собственных баз знаний
- **Multi-tenant** поддержка для enterprise

### Performance & Scaling
- **Horizontal scaling** с несколькими workers
- **Caching layer** для оптимизации повторных запросов
- **Rate limiting** для контроля нагрузки
- **Background task queues** для больших исследований

---

**🎯 AI Agent Farm - ваш надежный партнер для автоматизированных исследований с использованием искусственного интеллекта!**
