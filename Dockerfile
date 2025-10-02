FROM python:3.11-slim-bookworm

LABEL maintainer="AI Agent Farm"
LABEL description="AI Agent Farm - Debian 12 Bookworm based container"

WORKDIR /app

# Установка системных зависимостей для Debian 12 Bookworm
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Порт по умолчанию
EXPOSE 8000

# Команда по умолчанию
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
