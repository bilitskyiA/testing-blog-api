#!/bin/bash

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
gunicorn configs.wsgi:application -t 130 -w 2 -b 0.0.0.0:8000
