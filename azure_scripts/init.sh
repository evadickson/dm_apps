#!/bin/bash
service ssh start
git rev-parse --short HEAD
python create_env_file_from_json.py "$ENVIRONMENT_NAME"
python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -b 0.0.0.0:8000 dm_apps.wsgi:application