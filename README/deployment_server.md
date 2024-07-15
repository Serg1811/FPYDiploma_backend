## Развертывание проекта на reg.ru
#### 1. На рег.ру заказать облачный сервер на Ubuntu.
#### 2. Привязать к серверу ваш ssh ключ.
#### 3. Запустить wsl если на windows, если на Linux просто открыть терминал.
#### 4. Прописать в терминале команду:
```
ssh root@ip_вашего_сервера 
```
#### 5. Указать пароль который пришел вам на почту.
#### 6. Создадим пользователя:
```
adduser имя_пользователя
```
#### 7. Назначим пользователя администратором:
```
usermod имя_пользователя -aG sudo
```
#### 8. Переключим на этого пользователя:
```
su имя_пользователя
```
#### 9. Переходим на рабочую директорию:
```
cd ~
```
#### 10. Обновим пакетный менеджер:
```
sudo apt update
sudo apt upgrade
```
#### 11. Установим необходимые пакеты:
```
sudo apt install python3.12-venv python3-pip postgresql nginx
sudo pip install poetry
```
#### 12. Запустим nginx:
```
sudo systemctl start nginx
```
Убедимся что запустился nginx
```
sudo systemctl status nginx
```
#### 13. Скачаем репозиторий GitHub:
```
git clone https_репозитория
```
#### 14. Перейдем в папку репозитория где лежит manage.py:
```
cd название_проекта
```
#### 15. Создадим БД. 
Переключимся на пользователя postgres:
```
sudo su postgres
```
Переключимся на psql
```
psql
```
Зададим пароль для postgres
```
ALTER USER postgres WITH PASSWORD 'ваш_пароль';
```
Создадим БД
```
CREATE DATABASE cloud_db; Или ваше название
```
Выйдем из psql
```
\q
```
Выходим из под пользователя postgres
```
exit
```
#### 16. Создадим .env на сервере:
Переходим в директории с Django проектом, там где находится файл manage.py
```
nano .env
```
Прописываем следующие параметры в файле .env
```
DEBUG=True(по умолчанию, потом поменять на False)
ALLOWED_HOSTS=localhost,127.0.0.1,ваш_ip
DB_NAME=название_вашей_БД
DB_HOST=localhost
DB_PORT=5432 (по умолчанию)
DB_USER=имя_пользователя
DB_PASSWORD=пароль_БД
```
#### 17. Настроим виртуальное окружение:
В той же директории с manage.py
```
python3.12 -m venv env
```
Активировуем виртуальное окружение
```
source env/bin/activate
```
Утановим необходимые пакеты из requirements.txt
```
poetry install
poetry add gunicorn
```
Выполним миграции:
```
python manage.py migrate
```
<!-- #### 18. Соберем статические файлы:
```
python manage.py collectstatic -->
```
#### 19. Запустим сервер:
```
python manage.py runserver 0.0.0.0:8000
```
В .env поменять DEBUG на False
```
DEBUG=False
```
#### 20. Настроим gunicorn:
```
gunicorn config.wsgi -b 0.0.0.0:8000
```
Создадим файл настроек gunicorn \
Переходим:
```
sudo nano /etc/systemd/system/gunicorn.service
```
Пропишем следующие настройки:
```
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=serg181182
Group=www-data
WorkingDirectory=/home/serg181182/FPYDiploma_backend
ExecStart=/home/serg181182/FPYDiploma_backend/env/bin/gunicorn --access-logfile -\
          --workers 3 \
          --bind unix:/home/serg181182/FPYDiploma_backend/config.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```
Зупстим:
```
sudo systemctl start gunicorn
```
```
sudo systemctl enable gunicorn
```
Проверим статус:
```
sudo systemctl status gunicorn
```


Дальше не получилось. Ответ на "sudo systemctl status gunicorn"  - "Active: failed"
Эту проблему пока не получилось решить.