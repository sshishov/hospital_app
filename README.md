# Hospital App

Django + MongoDB

## Installation (Docker):
 - go inside `docker/compose` folder
 - run `docker-compose up` (or `docker-compose up -d` to start in background)
 - connect from browser `http://localhost:8013/`

 
## Installation (Development):
## djongo requires Python '>=3.6 
 - go inside `docker/compose` folder
 - run `docker-compose up mongodb` (or `docker-compose up -d mongodb` to start in background)
 - after this to start MongoDB you should just type `docker-compose start mongodb`
 - create virtualenv with Python3 and install requirements:
 ```bash
 mkvirtualenv --python=python3.6 hospital_app
 pip install -r requirements/development.txt
 ```
 - run migrations and compile static
 ```bash
 python manage.py migrate
 python manage.py collectstatic --no-input
 python manage.py compilemessages -l ru
 ```
 - run development server `python manage.py runserver 8000`
 - connect from browser `http://localhost:8000/`
