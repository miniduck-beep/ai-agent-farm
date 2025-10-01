# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# --- ДОБАВЬТЕ ЭТУ СТРОКУ ---
# Устанавливаем PYTHONPATH, чтобы Python всегда знал, где искать наши модули
ENV PYTHONPATH=/code
# ---------------------------

# Копируем файл с зависимостями и устанавливаем их
# Это делается отдельно для использования кэширования слоев Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копируем весь код приложения
COPY ./app ./app
COPY main.py .

# Порт, который будет слушать Streamlit
EXPOSE 8501