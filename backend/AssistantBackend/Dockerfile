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



RUN apt-get update && \
    apt-get install -y wget unzip


# Копируем проект
COPY . /app

# Создаем директорию для модели
RUN mkdir -p /app/AssistantBackend/AssistantBackend

# Скачивание и распаковка модели
RUN wget http://vectors.nlpl.eu/repository/20/65.zip -O /tmp/model.zip
RUN  unzip -j /tmp/model.zip 'model.bin' -d /app/AssistantBackend/AssistantBackend/
RUN echo herelll "$PWD"
RUN rm /tmp/model.zip





CMD  python manage.py runserver 0.0.0.0:8000
# Запускаем Django
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
