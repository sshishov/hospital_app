# Hospital App

Django + MongoDB

## Installation:

 - copy `docker-compose` template from `docker` folder + additional files from this folder
 - configure paths properly to link user-creation script and future data folder
 - run `docker-compose up` (or `docker-compose up -d` to start in background)
 - after this to start MongoDB you should just type `docker-compose start mongodb`
 - create virtualenv with Python3 and install requirements:
 ```
 mkvirtualenv --python=python3 hospital_app
 pip install -r requirements/python/development.txt
 ```
 - run development server `python manage.py runserver 8000`
 - connect from browser `http://localhost:8000/`