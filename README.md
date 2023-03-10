# Описание

Данный проект является RESTful API, написанный на python-фреймворке FastApi, который выполняется все CRUD запросы к базе данных через HTTP-запросы

# Требования

В качестве СУБД используется PostgreSQL, которая будет развернута в Docker Compose, который входит в состав Docker (Скачать Docker можно по [ссылке](https://docs.docker.com/get-docker/)). Используемые библиотеки хранятся в файле requirements.txt.

# Установка необходимых компонентов

Чтобы установить необходимые библиотеки, выполните команду `$ pip install -r requirements.txt`
```
  fastapi==0.89.1
  uvicorn==0.20.0
  sqlalchemy==1.4.46
  alembic==1.9.2
  psycopg2-binary==2.9.5
```

# Развертывание PostgreSQL

Для того, чтобы развернуть базу данных, необходимо развернуть СУБД в Docker Compose, для этого необходимо выполнить следующие команды
```
  $ sudo docker compose up -d
```
> Если пишет, что данный адрес уже используется, то просмотрите с помощью команды `sudo ss -lptn 'sport = :<PORT>'` какой процесс использует данный адрес и остановите процесс с помощью команды `kill <PID>`, либо измените адрес или порт в файле `.env`

Проверьте существование контейнера с помощью команды 
```
  $ sudo docker compose ps
```

# Запуск сервера и миграция базы данных

Для запуска нашего RESTful API необходимо запустить `uvicorn`:
```
  $ alembic upgrade head
  $ uvicorn api.v1.main:api
```
