# ===========================================
# AI Agent Farm - Production-Ready Dockerfile
# ===========================================

FROM python:3.11-slim

# Обновляем систему и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /code

# 🔒 БЕЗОПАСНОСТЬ: Создаем непривилегированного пользователя
RUN groupadd -r appgroup && useradd -r -g appgroup -d /code -s /bin/bash appuser

# Копируем и устанавливаем зависимости (делаем это до USER для кеширования слоев)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY ./app ./app

# 🔒 БЕЗОПАСНОСТЬ: Меняем владельца всех файлов на appuser
RUN chown -R appuser:appgroup /code

# 🔒 БЕЗОПАСНОСТЬ: Переключаемся на непривилегированного пользователя
USER appuser

# Устанавливаем переменные окружения
ENV PYTHONPATH="/code"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Указываем порт для FastAPI
EXPOSE 8000

# 🚀 Команда запуска с оптимизациями для production
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
