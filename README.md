Важное

Запуск celery( --pool=solo for windows):
celery -A app.tasks.celery_app:celery_app worker -l INFO --pool=solo

