## Prerequisites
* Create Python `virtualenv`.
* Install [redis] required for `python-channels`

## Start redis

    $ redis-server --daemonize yes

## Django
In this directory and highly recommended in a Python virtual environment, run

### Install dependencies

    $ pip install -r requirements/local.pip

### Create the database tables and initial data
we are using it because we use django session that store at db but don't worry it store at `sqlite`.

    $ python manage.py migrate

### Start the application

    $ python manage.py runserver

### API Documentation

    https://documenter.getpostman.com/view/869878/SWLe8oWc