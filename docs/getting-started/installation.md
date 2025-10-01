# 📦 Установка

Подробная инструкция по установке AI Agent Farm в различных окружениях.

## Системные требования

- **OS**: Linux, macOS, Windows
- **Python**: 3.11 или выше
- **Docker**: 20.10 или выше (рекомендуется)
- **RAM**: минимум 2GB, рекомендуется 4GB+
- **Диск**: минимум 5GB свободного места

## Docker установка (Рекомендуется)

### Стандартная установка
```bash
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
cp .env.example .env
docker compose up -d
```

### С VPN поддержкой
Для обхода геоблокировок Gemini API:
```bash
docker compose -f docker-compose.vpn.yml up -d
```

## Локальная установка

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv redis-server
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS
```bash
brew install python@3.11 redis
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```powershell
# Установите Python 3.11 с python.org
# Установите Redis через WSL или Docker
git clone https://github.com/miniduck-beep/ai-agent-farm.git
cd ai-agent-farm
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Конфигурация API ключей

### Получение Gemini API ключа
1. Перейдите на https://makersuite.google.com/app/apikey
2. Создайте новый API ключ
3. Добавьте в `.env`: `GOOGLE_API_KEY=your_key`

### Получение Serper API ключа
1. Зарегистрируйтесь на https://serper.dev
2. Получите API ключ в dashboard
3. Добавьте в `.env`: `SERPER_API_KEY=your_key`

## Проверка установки

```bash
# Проверка API
curl http://localhost:8000/

# Проверка статуса системы
curl http://localhost:8000/status

# Тестовое исследование
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test"}'
```

## Устранение проблем

### Проблемы с Docker
```bash
# Перезапуск контейнеров
docker compose down && docker compose up -d

# Просмотр логов
docker compose logs -f
```

### Проблемы с зависимостями
```bash
# Обновление pip
pip install --upgrade pip

# Переустановка зависимостей
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Проблемы с Redis
```bash
# Ubuntu/Debian
sudo systemctl restart redis-server

# macOS
brew services restart redis

# Docker
docker compose restart redis
```

## Следующие шаги

После успешной установки:
1. [Настройте конфигурацию](configuration.md)
2. [Изучите быстрый старт](quick-start.md)
3. [Интегрируйтесь с n8n](../guides/n8n-integration.md)
