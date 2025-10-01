# AI Agent Farm

**Добро пожаловать в AI Agent Farm** — мощную многоагентную систему для автоматизированных исследований и генерации контента!

## Что такое AI Agent Farm?

AI Agent Farm — это современная платформа, которая объединяет силу многоагентных ИИ-систем с удобными API и инструментами автоматизации. Система позволяет создавать специализированные команды ИИ-агентов для решения сложных исследовательских задач, генерации контента и бизнес-аналитики.

## ✨ Ключевые возможности

### 🎯 Многоагентная архитектура
- **Исследователь**: Поиск и анализ актуальной информации
- **Писатель**: Создание структурированных отчетов  
- **Супервизор**: Контроль качества и финальная проверка

### 🏗️ Специализированные команды агентов
- 💼 **Business Analyst Team**: Рыночные исследования и бизнес-анализ
- 📝 **Content Marketing Team**: SEO-стратегии и контент-планы  
- 🔬 **Tech Research Team**: Технические исследования и архитектура
- 💰 **Financial Analysis Team**: Финансовый анализ и инвестиционные возможности
- 🚀 **Startup Consultant Team**: Бизнес-модели и go-to-market стратегии

### 🔄 Полная автоматизация
- **n8n интеграция**: Готовые workflow для автоматизации
- **Асинхронная обработка**: Celery + Redis для масштабируемости
- **REST API**: Простое подключение к любым системам
- **Real-time мониторинг**: Отслеживание прогресса выполнения

## 🚀 Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm

# Настраиваем окружение
cp .env.example .env
# Отредактируйте .env файл

# Запускаем систему
docker compose up -d

# Проверяем статус
curl http://localhost:8000/
```

## 📚 Документация

- **[Быстрый старт](getting-started/quick-start.md)** — начните работу за 5 минут
- **[API Документация](api/overview.md)** — полное описание API
- **[Руководства](guides/n8n-integration.md)** — пошаговые инструкции
- **[Архитектура](architecture/overview.md)** — техническая документация

## 💡 Примеры использования

### Простое исследование
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Искусственный интеллект в образовании"}'
```

### Специализированная команда
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Рынок электромобилей",
    "crew_type": "business_analyst",
    "depth": "deep"
  }'
```

## 🤝 Сообщество

- 💬 [GitHub Discussions](https://github.com/miniduck-beep/ai-agent-farm/discussions)
- 🐛 [Issues](https://github.com/miniduck-beep/ai-agent-farm/issues)
- 🎭 [Discord сервер](https://discord.gg/ai-farm)

## 📄 Лицензия

AI Agent Farm распространяется под [MIT лицензией](https://github.com/miniduck-beep/ai-agent-farm/blob/main/LICENSE).

---

**Готовы начать?** Переходите к разделу [Быстрый старт](getting-started/quick-start.md)!
