# 🤝 Вклад в AI Agent Farm

Спасибо за интерес к развитию AI Agent Farm! Мы ценим любой вклад в проект - от сообщений об ошибках до крупных функций.

## 📋 Содержание

- [🐛 Сообщение об ошибках](#-сообщение-об-ошибках)
- [💡 Предложение улучшений](#-предложение-улучшений)  
- [🛠️ Настройка окружения разработки](#️-настройка-окружения-разработки)
- [📝 Процесс разработки](#-процесс-разработки)
- [🧪 Тестирование](#-тестирование)
- [📚 Документация](#-документация)
- [🎭 Создание новых агентов](#-создание-новых-агентов)
- [📦 Pull Request Guidelines](#-pull-request-guidelines)
- [🎨 Стандарты кода](#-стандарты-кода)
- [🏷️ Commit Messages](#️-commit-messages)

---

## 🐛 Сообщение об ошибках

Если вы нашли ошибку, пожалуйста:

### Перед созданием Issue:
- Проверьте [открытые Issues](https://github.com/miniduck-beep/ai-agent-farm/issues) - возможно, ошибка уже известна
- Убедитесь, что используете актуальную версию проекта
- Попробуйте воспроизвести ошибку с минимальным примером

### Что включить в отчет:
- **Краткое описание** ошибки
- **Шаги для воспроизведения** (детально)
- **Ожидаемое поведение**
- **Фактическое поведение**
- **Версия системы** (ОС, Python, Docker)
- **Логи и трассировки** (если есть)
- **Конфигурация** (без секретов!)

### Шаблон Issue:

```markdown
**Описание ошибки**
Краткое описание проблемы.

**Воспроизведение**
1. Выполните команду `...`
2. Откройте `...`
3. Увидите ошибку

**Ожидаемое поведение**
Что должно было произойти.

**Скриншоты**
При необходимости добавьте скриншоты.

**Окружение:**
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.11.0]
- Docker: [e.g. 20.10.21]
- Версия проекта: [e.g. v1.0.0]

**Логи**
```
Вставьте соответствующие логи
```

**Дополнительный контекст**
Любая другая информация о проблеме.
```

---

## 💡 Предложение улучшений

Мы приветствуем предложения новых функций!

### Перед созданием предложения:
- Проверьте [Roadmap](README.md#-roadmap) - возможно, функция уже запланирована
- Обсудите идею в [Discussions](https://github.com/miniduck-beep/ai-agent-farm/discussions)
- Убедитесь, что функция подходит философии проекта

### Что включить в предложение:
- **Проблема**, которую решает функция
- **Предлагаемое решение** с деталями
- **Альтернативы**, которые вы рассматривали
- **Примеры использования**
- **API или интерфейс** (если применимо)

---

## 🛠️ Настройка окружения разработки

### 1. Fork и клонирование

```bash
# Fork репозиторий через GitHub UI
# Затем клонируйте ваш fork
git clone https://github.com/YOUR_USERNAME/ai-agent-farm.git
cd ai-agent-farm

# Добавьте upstream репозиторий
git remote add upstream https://github.com/miniduck-beep/ai-agent-farm.git
```

### 2. Настройка окружения

```bash
# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установите зависимости разработки
pip install -r requirements-dev.txt

# Установите pre-commit hooks
pre-commit install
```

### 3. Конфигурация

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env для добавления ваших API ключей
# Для разработки можно использовать тестовые ключи
```

### 4. Запуск в режиме разработки

```bash
# Запустите Redis (в отдельном терминале)
redis-server

# Запустите API в режиме hot-reload
uvicorn app.api:app --reload --port 8000

# Запустите Celery worker (в отдельном терминале)
celery -A app.tasks worker --loglevel=debug
```

### 5. Проверка установки

```bash
# Проверьте статус API
curl http://localhost:8000/

# Запустите тесты
pytest

# Проверьте качество кода
black . --check
flake8 .
```

---

## 📝 Процесс разработки

### 1. Создание feature branch

```bash
# Обновите main ветку
git checkout main
git pull upstream main

# Создайте feature branch
git checkout -b feature/amazing-feature
# или
git checkout -b bugfix/fix-something
# или  
git checkout -b docs/improve-readme
```

### 2. Разработка

- Следуйте [стандартам кода](#-стандарты-кода)
- Пишите тесты для новой функциональности
- Обновляйте документацию при необходимости
- Делайте атомарные commits с [хорошими сообщениями](#️-commit-messages)

### 3. Подготовка к отправке

```bash
# Убедитесь, что тесты проходят
pytest

# Проверьте качество кода
black .
flake8 .
mypy .

# Запустите pre-commit hooks
pre-commit run --all-files

# Обновите main и rebase (при необходимости)
git checkout main
git pull upstream main
git checkout feature/amazing-feature
git rebase main
```

---

## 🧪 Тестирование

### Структура тестов

```
tests/
├── unit/           # Юнит-тесты отдельных функций
├── integration/    # Тесты интеграции компонентов
├── e2e/           # End-to-end тесты API
├── fixtures/      # Фикстуры для тестов
└── conftest.py    # Общие настройки pytest
```

### Запуск тестов

```bash
# Все тесты
pytest

# Определенная категория
pytest tests/unit/
pytest tests/integration/

# С покрытием кода
pytest --cov=app --cov-report=html

# Только тесты, связанные с изменениями
pytest --lf
```

### Написание тестов

```python
import pytest
from app.api import app
from fastapi.testclient import TestClient

def test_research_endpoint():
    """Тест создания исследования через API"""
    client = TestClient(app)
    
    response = client.post(
        "/research",
        json={"topic": "Тестовая тема"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "PENDING"
```

### Требования к тестам

- **Покрытие**: новый код должен иметь покрытие тестами ≥90%
- **Изоляция**: тесты не должны зависеть друг от друга
- **Мокинг**: используйте моки для внешних API
- **Данные**: не используйте реальные API ключи в тестах

---

## 📚 Документация

### Типы документации

- **README**: общий обзор и quick start
- **API docs**: автоматическая генерация из кода
- **Guides**: пошаговые руководства в `docs/guides/`
- **Architecture**: техническая документация в `docs/architecture/`
- **Examples**: примеры использования в `docs/examples/`

### Стандарты документации

- Используйте Markdown для всех документов
- Включайте примеры кода для API
- Добавляйте диаграммы для сложных концепций
- Обновляйте документацию вместе с кодом

### Docstrings

```python
def create_research_task(topic: str, crew_type: str = "general") -> str:
    """Создает новую задачу исследования.
    
    Args:
        topic: Тема для исследования
        crew_type: Тип команды агентов для использования
        
    Returns:
        ID созданной задачи
        
    Raises:
        ValidationError: Если тема пустая или недопустимый crew_type
        
    Example:
        >>> task_id = create_research_task("AI в образовании", "tech_research")
        >>> print(task_id)
        "abc123-def456"
    """
```

---

## 🎭 Создание новых агентов

### Структура агента

```python
# app/agents/new_agent_type.py
from crewai import Agent, Task
from app.agents.base import BaseAgentTeam

class NewAgentTeam(BaseAgentTeam):
    """Команда агентов для новой специализации."""
    
    def create_agents(self):
        """Создает агентов для команды."""
        self.researcher = Agent(
            role="Специализированный исследователь",
            goal="Конкретная цель исследования",
            backstory="Детальная предыстория агента",
            tools=self.tools,
            llm=self.llm
        )
        
        self.analyst = Agent(
            role="Аналитик",
            goal="Анализ собранной информации",
            backstory="Опыт в области анализа",
            tools=self.tools,
            llm=self.llm
        )
    
    def create_tasks(self, topic: str):
        """Создает задачи для агентов."""
        return [
            Task(
                description=f"Исследование темы: {topic}",
                agent=self.researcher,
                expected_output="Детальный отчет исследования"
            ),
            Task(
                description=f"Анализ результатов по теме: {topic}",
                agent=self.analyst,
                expected_output="Структурированный анализ",
                dependencies=[0]  # Зависит от первой задачи
            )
        ]
```

### Регистрация агента

```python
# app/agents/__init__.py
from .new_agent_type import NewAgentTeam

AGENT_TEAMS = {
    "general": GeneralTeam,
    "new_type": NewAgentTeam,  # Добавьте здесь
}
```

### Документация агента

Создайте документ `docs/agents/new-agent-type.md`:

```markdown
# New Agent Type Team

## Описание
Подробное описание специализации команды.

## Агенты
- **Researcher**: роль и функции
- **Analyst**: роль и функции

## Примеры использования
```bash
curl -X POST "http://localhost:8000/research" \
  -d '{"topic": "Example topic", "crew_type": "new_type"}'
```

## Лучшие практики
Рекомендации по использованию команды.
```

---

## 📦 Pull Request Guidelines

### Перед созданием PR

- [ ] Код соответствует стандартам проекта
- [ ] Все тесты проходят
- [ ] Добавлены тесты для новой функциональности
- [ ] Обновлена документация
- [ ] Проверена совместимость с существующим API
- [ ] Нет конфликтов с main веткой

### Описание PR

```markdown
## Описание
Краткое описание изменений и их цель.

## Тип изменения
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (функция, которая ломает совместимость)
- [ ] Documentation update

## Тестирование
- [ ] Добавлены unit тесты
- [ ] Добавлены integration тесты
- [ ] Протестировано вручную

## Чеклист
- [ ] Код следует стилю проекта
- [ ] Проведена самопроверка кода
- [ ] Обновлена документация
- [ ] Изменения не ломают существующие тесты
```

### Review процесс

1. **Автоматические проверки**: CI должен пройти успешно
2. **Code review**: как минимум одобрение от мейнтейнера
3. **Manual testing**: тестирование критических изменений
4. **Documentation review**: проверка документации

---

## 🎨 Стандарты кода

### Python стиль

```python
# Хорошо
def create_agent_team(crew_type: str, tools: List[Tool]) -> BaseAgentTeam:
    """Создает команду агентов указанного типа."""
    if crew_type not in AGENT_TEAMS:
        raise ValueError(f"Unknown crew type: {crew_type}")
    
    team_class = AGENT_TEAMS[crew_type]
    return team_class(tools=tools)

# Плохо  
def createAgentTeam(crewType,tools):
    if crewType not in AGENT_TEAMS:raise ValueError("Unknown crew type: "+crewType)
    teamClass=AGENT_TEAMS[crewType]
    return teamClass(tools=tools)
```

### Инструменты качества кода

```bash
# Форматирование кода
black . --line-length 88

# Проверка стиля
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Проверка типов
mypy . --ignore-missing-imports

# Сортировка импортов
isort . --profile black
```

### Конфигурация в pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
```

---

## 🏷️ Commit Messages

### Формат

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Типы commits

- **feat**: новая функциональность
- **fix**: исправление ошибки
- **docs**: изменения в документации
- **style**: форматирование, точки с запятой и т.д.
- **refactor**: рефакторинг кода
- **test**: добавление тестов
- **chore**: обновление сборочных задач, конфигурации и т.д.

### Примеры

```bash
feat(agents): add financial analysis agent team

- Add FinancialAnalysisTeam with specialized agents
- Include financial metrics calculation tools
- Add tests for financial analysis workflows

Closes #123

fix(api): handle empty topic validation

- Add validation for empty research topics
- Return 400 status code with clear error message
- Add test cases for edge cases

docs(readme): update installation instructions

- Add Docker compose instructions
- Include VPN setup section
- Fix typos in API examples
```

---

## 🚀 После принятия PR

### Для контрибьюторов

1. **Удалите feature branch** после merge
2. **Обновите свой fork** с upstream
3. **Отметьтесь в Contributors** (автоматически)

### Для мейнтейнеров

1. **Обновите CHANGELOG** с описанием изменений
2. **Создайте release** если накопилось достаточно изменений
3. **Обновите документацию** на сайте проекта
4. **Отправьте благодарность** контрибьютору

---

## 🎯 Приоритетные задачи

Ищете что-то для начала? Проверьте Issues с метками:

- 🟢 **good first issue**: подходит для новичков
- 🔵 **help wanted**: нужна помощь сообщества
- 🟡 **enhancement**: улучшения функциональности
- 🔴 **bug**: исправления ошибок

---

## 📞 Вопросы?

Если у вас есть вопросы о процессе разработки:

- 💬 Создайте [Discussion](https://github.com/miniduck-beep/ai-agent-farm/discussions)
- 📧 Напишите нам: [dev@ai-farm.dev](mailto:dev@ai-farm.dev)
- 🎭 Присоединяйтесь к [Discord сообществу](https://discord.gg/ai-farm)

---

**Спасибо за ваш вклад в AI Agent Farm! 🚀**

*Каждый PR делает проект лучше для всего сообщества.*
