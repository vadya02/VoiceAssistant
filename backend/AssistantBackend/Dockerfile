# Используем базовый образ Python
FROM python:3.9
RUN apt-get update && apt-get install -y ffmpeg
# Устанавливаем рабочую директорию
WORKDIR /app

# Отключаем кэширование pyc-файлов и буферизацию
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем и устанавливаем зависимости
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app
# WORKDIR /app/AssistantBackend
# Выполняем миграции (если нужно)
# RUN python manage.py migrate

# Запускаем Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
