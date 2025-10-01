# 🚀 Инструкции по публикации AI Agent Farm на GitHub

## Шаг 1: Создание репозитория на GitHub

1. Перейдите на https://github.com/miniduck-beep
2. Нажмите "New repository" (зеленая кнопка)
3. Заполните данные:
   - **Repository name**: `ai-agent-farm`
   - **Description**: `🤖 Мощная многоагентная система для автоматизированных исследований и генерации контента`
   - **Public** (отметьте, чтобы сделать Open Source)
   - **НЕ добавляйте** README, .gitignore или license (у нас уже есть)

## Шаг 2: Загрузка кода

Выполните команды в терминале из папки `/home/su/ai-farm`:

```bash
# Подключаем удаленный репозиторий
git remote add origin https://github.com/miniduck-beep/ai-agent-farm.git

# Загружаем код на GitHub
git push -u origin main
```

## Шаг 3: Настройка GitHub репозитория

### 3.1 Описание и теги
1. Перейдите в Settings → General
2. В разделе "About" добавьте:
   - **Description**: `🤖 Мощная многоагентная система для автоматизированных исследований`
   - **Website**: `https://miniduck-beep.github.io/ai-agent-farm`
   - **Topics**: `ai`, `agents`, `multi-agent`, `research`, `automation`, `crewai`, `fastapi`, `python`

### 3.2 Включение Issues и Discussions
1. Settings → General → Features
2. Отметьте: ✅ Issues, ✅ Discussions

### 3.3 Настройка GitHub Pages (для документации)
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / root (создастся автоматически при первом пуше документации)

### 3.4 Защита main ветки
1. Settings → Branches
2. Add rule для `main`:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass before merging

## Шаг 4: Секреты для CI/CD (опционально)

Если планируете автоматический деплой Docker образов:
1. Settings → Secrets and variables → Actions
2. Добавьте:
   - `DOCKER_USERNAME`: ваш Docker Hub username
   - `DOCKER_PASSWORD`: ваш Docker Hub password/token

## Шаг 5: Создание первого релиза

1. Releases → Create a new release
2. Tag version: `v1.0.0`
3. Release title: `🚀 AI Agent Farm v1.0.0 - Initial Release`
4. Описание:
```markdown
## 🎉 Первый стабильный релиз AI Agent Farm!

### ✨ Ключевые возможности:
- 🤖 Многоагентные команды исследователей
- 🔄 REST API с FastAPI и асинхронной обработкой
- 🎭 5 специализированных типов команд агентов
- 🔗 Готовая интеграция с n8n
- 🌐 VPN поддержка для обхода геоблокировок
- 🐳 Docker контейнеризация
- 📚 Комплексная документация

### 🚀 Быстрый старт:
```bash
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
cp .env.example .env
# Отредактируйте .env
docker compose up -d
```

Полная документация: https://miniduck-beep.github.io/ai-agent-farm
```

## Шаг 6: Проверка работы CI/CD

После пуша должны автоматически запуститься:
- ✅ Тесты (pytest, flake8, black, mypy)
- ✅ Сборка Docker образа
- ✅ Security сканирование
- ✅ Сборка документации

## 🎯 Результат

После выполнения всех шагов у вас будет:
- ✅ Профессиональный Open Source проект
- ✅ Автоматическое тестирование и сборка
- ✅ Красивая документация на GitHub Pages
- ✅ Готовность к контрибьютам сообщества

---

**🚀 Успешной публикации!**
