# MIT_backend

[![Build Status](https://travis-ci.org/MentorInTech/MIT_backend.svg?branch=develop)](https://travis-ci.org/MentorInTech/MIT_backend)
[![Coverage Status](https://coveralls.io/repos/github/MentorInTech/MIT_backend/badge.svg?branch=organize-project)](https://coveralls.io/github/MentorInTech/MIT_backend?branch=organize-project)

## Quick start

```
$ git clone https://github.com/MentorInTech/MIT_backend
$ cd MIT_backend
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt

# If you use bash:
$ export DJANGO_SETTINGS_MODULE=config.settings.local
$ export DATABASE_NAME=mit
$ export DATABASE_USER=postgres
$ export DATABASE_PASSWORD=""
# If you use fish
$ set -x DJANSO_SETTINGS_MODULE config.settings.local
$ set -x DATABASE_NAME mit
$ set -x DATABASE_USER postgres
$ set -x DATABASE_PASSWORD ""

$ python manage.py migrate
$ python manage.py runserver
```

Go to `http://localhost:8000` on your browser. APIs are browseable, and you can 
also checkout the Swagger API doc on `http://localhost:8000/docs/`.

## Prerequisites

* Python > 3.6
* Postgres
* Redis

## Installation

### Virtual environment

After cloning this repo into your local machine, we first need to
create an isolated environment, or a "virtual environment" in the Python
terminology, to safely resolve the dependencies. In the Quick Start,
we use the built-in tooling called `venv` to accomplish that. However,
the recommended way from the [python.org](https://www.python.org)
is to use [`pipenv`](https://docs.pipenv.org/). Follow their installation
guide to install it first.

Once you have `pipenv`, inside the project root directory:

```
$ pipenv install --dev
```

This creates a virtual environment and installs all the development
dependencies described in the Pipfile. Let's activate the
virtual environment: 

```
$ pipenv shell
(MIT_backend_xxxxxxx) $ 
```

Once you activate the virtual environment, you'll see your prompt
prepended with the virtual environment name `pipenv` created.
Now when we install another PyPI package via `pip`, it'll be installed
only for our project. This concept of isolated environment is important
for building repeatable application.

### Postgres

The database of choice is Postgres. Install it if you haven't done so.
For Mac user, install [Postgress.app](https://postgresapp.com/) is recommended.
By default, a database user, named by your system user name with empty password
is created. Also, a database named by your system user name is created.
It's your choice to use the database/user or create your own for the app
development.

### Redis

Redis is useful for caching and as a message broker. Currently it's
only been used as the message broker for running background tasks using
celery.

### Configuration

Here's a list of environment variables you need to set before running the application:

* `DJANGO_SETTINGS_MODULE` - for local development, use `config.settings.local`
* `DATABASE_NAME` - use your system user name
* `DATABASE_USER` - use your system user name
* `DATABASE_PASSWORD` - use empty string

#### Tips to manage environment variables with `pipenv`

If you use `pipenv` to manage the virtual environment, you can put the environment
variables into the `.env` file such that:

```
$ cat .env
DJANGO_SETTINGS_MODULE=config.settings.local
DATABASE_NAME=mit
DATABASE_USER=mit
DATABASE_PASSWORD=""
```

`pipenv` automatically loads the variables when you activate it:

```
$ pipenv shell
(MIT_backend_xxxxxxx) $ echo $DJANGO_SETTINGS_MODULE
config.settings.local
```

### Database migration

Use the commands to migrate your database:

```
$ python manage.py migrate
```

## Commands

### Test

Run tests to make sure everything's set up correctly till this point:

```
$ python manage.py test
```

### Start server

Start the development server at localhost:8000

```
$ python manage.py runserver
```

### Celery

This app comes with Celery.

To run a celery worker:

```
celery -A MIT_backend.tasks worker -l info
```

Please note: For Celery's import magic to work, it is important where the
celery commands are run. If you are in the same folder with manage.py,
you should be right.

## Project layout

The project layout is influenced by [@pydanny](https://twitter.com/pydanny)'s
[cookiecutter-django](https://github.com/pydanny/cookiecutter-django)
project. Instead of the Django's built-in startproject command to scaffold
our project, the application code is split from the configuration code.

```
MIT_backend/ : project root
  |
  |--config/ : all the configurations and settings
  |
  |--MIT_backend/ : application root
```

If you want to create new apps for this Django project, create it in the
application root instead of the project root.

## Resources

1. [Django official tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
1. [Django Rest Framework (DRF) tutorial](http://www.django-rest-framework.org/tutorial/1-serialization/)
1. [Authentication with Djoser](http://djoser.readthedocs.io/en/stable/)
1. [Celery - First steps with Django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
