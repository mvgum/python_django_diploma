FROM python:3.11-slim

# Устанавливаем системные зависимости для работы Pillow (картинки) и psycopg2 (если перейдете на PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# По умолчанию запускаем Celery (это можно переопределить в docker-compose)
CMD ["celery", "-A", "config", "worker", "-l", "info"]