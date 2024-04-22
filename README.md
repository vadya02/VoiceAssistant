# VoiceAssistant

## Настройка клиентской части




## Настройка серверной части
Чтобы запустить Django-бэкенд на своем компьютере, выполните следующие шаги. Они включают установку необходимых инструментов, создание и активацию виртуального окружения, установку зависимостей и запуск вашего Django-приложения.

#Предварительные требования
 - Убедитесь, что на вашем компьютере установлен Python (рекомендуется Python 3.7 или выше).
 - Установите пакетный менеджер pip, который обычно идет вместе с установкой Python.
 - Убедитесь, что у вас установлена БД Postgresql
 - Скачайте модель word2vec "Национальный корпус русского языка" под номером 65 с сайта http://vectors.nlpl.eu/repository/
#Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/vadya02/VoiceAssistant.git

cd VoiceAssistant
```
## Шаг 2: Создание виртуального окружения
Для изоляции зависимостей создайте виртуальное окружение. Убедитесь, что у вас установлен virtualenv или venv.


Используйте venv, встроенный в Python 3
```python
python -m venv venv
```
Активируйте виртуальное окружение
- Для Windows:
```
venv\Scripts\activate
```
- Для Linux/macOS:
```
source venv/bin/activate
```
После активации виртуального окружения вы должны увидеть префикс (venv) в командной строке.

## Шаг 3: Установка зависимостей
```python
pip install -r requirements.txt
```
## Шаг 4: Настройка переменных окружения
Создайте файл .env в папке /backend

Задайте следующие переменные:
```
DB_NAME='имя_бд'
USER='имя_пользователя'
PASSWORD='пароль'
HOST='хост'
PORT='порт'
```
## Шаг 5: Применение миграций
Перед запуском сервера Django, примените миграции к базе данных, чтобы создать необходимые таблицы:
```python
python manage.py migrate
```
## Шаг 6: Запуск сервера
Теперь вы готовы запустить сервер Django:
```python
python manage.py runserver
```

## Шаг 7: Деактивация виртуального окружения (по желанию)
Когда вы закончите работу с проектом, вы можете деактивировать виртуальное окружение:
```python
deactivate
```
На этом все! Теперь у вас есть общая инструкция по настройке и запуску Django-бэкенда на своем компьютере. Если у вас есть дополнительные шаги или специфические требования, не забудьте их добавить к этой документации.
