# MIT_backend

[![Build Status](https://travis-ci.org/MentorInTech/MIT_backend.svg?branch=develop)](https://travis-ci.org/MentorInTech/MIT_backend)
[![Coverage Status](https://coveralls.io/repos/github/MentorInTech/MIT_backend/badge.svg?branch=organize-project)](https://coveralls.io/github/MentorInTech/MIT_backend?branch=organize-project)

## Quick start

```
git clone https://github.com/MentorInTech/MIT_backend
python3 -m venv .env
source .env/bin/activate
pip install requirements.txt

python manage.py migrate
python manage.py runserver
```

Go to `http://localhost:8000` on your browser. APIs are browseable, and you can 
also checkout the Swagger API doc on `http://localhost:8000/docs/`.
