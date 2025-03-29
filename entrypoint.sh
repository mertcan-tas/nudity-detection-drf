python manage.py safe --noinput
python manage.py collectstatic --noinput --clear


exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application