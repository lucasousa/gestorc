web: gunicorn gestorc.wsgi --log-file -
celery: celery -A gestorc worker -l info
redis: redis-server