# 🧪 Руководство по тестированию - AI Agent Farm

> **Comprehensive фреймворк тестирования для обеспечения качества и надежности системы**

## 📋 Обзор

AI Agent Farm использует современный фреймворк тестирования на основе pytest, который включает три уровня тестов:
- **Unit тесты** - быстрые тесты отдельных компонентов
- **Integration тесты** - тестирование взаимодействия между компонентами  
- **End-to-End тесты** - полные сквозные тесты workflow

## 🚀 Быстрый старт

### Установка зависимостей
```bash
# Основные зависимости для тестирования
pip install pytest pytest-asyncio httpx pytest-mock pytest-cov

# Или через Makefile
make install-dev
```

### Запуск всех тестов
```bash
# Простой запуск
pytest

# Или через Makefile
make test
```

## 🎯 Типы тестов

### 1. Unit тесты (`tests/unit/`)
**Цель:** Тестирование отдельных функций и методов  
**Скорость:** Очень быстрые (< 1 сек на тест)  
**Изоляция:** Полная, с использованием моков

```bash
# Запуск только unit тестов
make test-unit
# или
pytest -m unit
```

**Что тестируется:**
- ✅ API endpoints и их ответы
- ✅ Валидация входных данных
- ✅ Обработка ошибок
- ✅ Pydantic модели
- ✅ Утилитарные функции

### 2. Integration тесты (`tests/integration/`)
**Цель:** Тестирование взаимодействия между компонентами  
**Скорость:** Средние (1-5 сек на тест)  
**Изоляция:** Частичная, реальные взаимодействия между модулями

```bash
# Запуск только integration тестов
make test-integration
# или
pytest -m integration
```

**Что тестируется:**
- ✅ Фабрика команд агентов (CrewFactory)
- ✅ Создание и выполнение динамических задач
- ✅ Интеграция API с Celery
- ✅ Работа с различными типами команд

### 3. End-to-End тесты (`tests/e2e/`)
**Цель:** Полное тестирование пользовательских сценариев  
**Скорость:** Медленные (5-30 сек на тест)  
**Изоляция:** Минимальная, максимально близко к production

```bash
# Запуск только e2e тестов
make test-e2e
# или
pytest -m e2e
```

**Что тестируется:**
- ✅ Полный workflow: создание → выполнение → получение результата
- ✅ Работа с разными типами команд агентов
- ✅ Обработка ошибочных сценариев
- ✅ Интеграция всех компонентов системы

## ⚡ Команды для запуска

### Основные команды
```bash
make test              # Все тесты
make test-fast         # Быстрые тесты (исключает slow)
make test-coverage     # Тесты с отчетом покрытия
make clean             # Очистка временных файлов
```

### Детальные команды pytest
```bash
# По категориям
pytest -m unit                    # Только unit
pytest -m integration             # Только integration  
pytest -m e2e                     # Только e2e
pytest -m "not slow"              # Исключить медленные

# По файлам
pytest tests/unit/test_api.py      # Конкретный файл
pytest tests/integration/         # Вся папка

# С дополнительными опциями
pytest -v                         # Подробный вывод
pytest -s                         # Показать print()
pytest --tb=short                 # Короткий traceback
pytest -x                         # Остановиться на первой ошибке
```

## 📊 Покрытие кода

### Генерация отчетов
```bash
# HTML отчет (рекомендуется)
make test-coverage

# Открыть отчет
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Интерпретация результатов
- **Зеленый (>90%)** - отличное покрытие
- **Желтый (75-90%)** - хорошее покрытие  
- **Красный (<75%)** - требует внимания

### Цели покрытия
- **Общее покрытие:** >80%
- **Unit тесты:** >95% для core логики
- **Integration тесты:** >70% для взаимодействий
- **E2E тесты:** >50% для критических путей

## 🏗️ Структура тестов

### Организация файлов
```
tests/
├── conftest.py              # Общие фикстуры и настройки
├── unit/                    # Unit тесты
│   └── test_api.py         # Тесты API endpoints
├── integration/            # Integration тесты
│   └── test_crew_factory.py # Тесты фабрики команд
├── e2e/                    # End-to-end тесты
│   └── test_full_workflow.py # Полные сценарии
└── fixtures/               # Тестовые данные (опционально)
```

### Именование тестов
```python
# Хорошие имена тестов
def test_create_research_with_valid_data():
def test_api_returns_422_for_empty_topic():
def test_crew_factory_creates_business_analysis_crew():

# Плохие имена
def test_api():
def test_success():
def test_1():
```

## 🛠️ Написание тестов

### Unit тест - пример
```python
@pytest.mark.unit
def test_create_research_basic(client, mock_celery, sample_research_data):
    """Тест создания базового исследования"""
    request_data = sample_research_data["basic_request"]
    
    response = client.post("/research", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "PENDING"
```

### Integration тест - пример
```python
@pytest.mark.integration
def test_crew_factory_creates_business_crew(mock_llm, mock_tools):
    """Тест создания команды бизнес-аналитики"""
    factory = CrewFactory()
    
    crew = factory.create_business_analysis_crew()
    
    assert crew is not None
    assert len(crew.agents) == 3  # Аналитик + Финансист + Стратег
```

### E2E тест - пример
```python
@pytest.mark.e2e
def test_complete_workflow(client, mock_celery, helpers):
    """Тест полного workflow исследования"""
    # 1. Создаем исследование
    response = client.post("/research", json={
        "topic": "Test Research",
        "crew_type": "general"
    })
    task_id = response.json()["task_id"]
    
    # 2. Получаем результат
    result_response = client.get(f"/result/{task_id}")
    
    assert result_response.status_code == 200
```

## 🎛️ Конфигурация тестов

### pytest.ini настройки
```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra                    # Показать краткую сводку
    -q                     # Тихий режим
    --strict-markers       # Строгая проверка маркеров
    --tb=short            # Короткий traceback
    --cov=app             # Покрытие для папки app
    --cov-report=html     # HTML отчет
testpaths = tests         # Папка с тестами
markers =
    unit: Unit тесты
    integration: Integration тесты
    e2e: End-to-end тесты
    slow: Медленные тесты
```

### Фикстуры в conftest.py
```python
@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def sample_research_data():
    """Тестовые данные для исследований"""
    return {
        "basic_request": {
            "topic": "Test Topic",
            "crew_type": "general"
        }
    }
```

## 🔧 Лучшие практики

### ✅ DO - Хорошие практики
- **Используйте описательные имена** тестов
- **Тестируйте один аспект** за раз
- **Используйте маркеры** для категоризации
- **Мокайте внешние зависимости** (API, базы данных)
- **Следуйте паттерну AAA** (Arrange, Act, Assert)
- **Поддерживайте тесты** в актуальном состоянии

### ❌ DON'T - Плохие практики
- Не создавайте зависимости между тестами
- Не тестируйте реальные внешние API в unit тестах
- Не игнорируйте падающие тесты
- Не делайте тесты слишком сложными
- Не дублируйте логику production кода

### Паттерн AAA
```python
def test_example():
    # Arrange (Подготовка)
    data = {"topic": "Test"}
    
    # Act (Действие)
    response = client.post("/research", json=data)
    
    # Assert (Проверка)
    assert response.status_code == 200
```

## 🐛 Отладка тестов

### Полезные опции pytest
```bash
# Показать все print() statements
pytest -s

# Остановиться на первой ошибке
pytest -x

# Запустить последние упавшие тесты
pytest --lf

# Подробный traceback
pytest --tb=long

# Запустить конкретный тест
pytest tests/unit/test_api.py::test_health_endpoint
```

### Отладка с pdb
```python
def test_example():
    # Точка останова для отладки
    import pdb; pdb.set_trace()
    
    response = client.get("/health")
    assert response.status_code == 200
```

## 🔄 CI/CD Integration

### GitHub Actions пример
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: make test-coverage
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 📈 Мониторинг качества

### Метрики качества
- **Test Coverage:** >80%
- **Test Success Rate:** >95%
- **Test Execution Time:** <5 мин для полного suite
- **Code Quality:** Без критических замечаний линтера

### Регулярные проверки
```bash
# Ежедневная проверка
make test-fast quality

# Еженедельная полная проверка  
make test-coverage
```

## 🆘 Решение проблем

### Частые проблемы

**🔴 Проблема:** Тесты падают с ошибкой `AttributeError`  
**💡 Решение:** Проверьте правильность импортов и моков

**🔴 Проблема:** Низкое покрытие кода  
**💡 Решение:** Добавьте тесты для неохваченных веток кода

**🔴 Проблема:** Медленные тесты  
**💡 Решение:** Используйте маркер `@pytest.mark.slow` и моки

**🔴 Проблема:** Тесты работают по отдельности, но падают вместе  
**💡 Решение:** Проверьте побочные эффекты и глобальное состояние

### Получение помощи
- Запустите `pytest --help` для списка опций
- Изучите документацию [pytest.org](https://docs.pytest.org/)
- Проверьте логи в `pytest.log`

---

## 🎯 Заключение

Качественное тестирование - основа надежного программного обеспечения. AI Agent Farm использует современные практики тестирования для обеспечения стабильности и качества на всех уровнях системы.

**Помните:** Хорошие тесты - это инвестиция в будущее проекта! 🚀
