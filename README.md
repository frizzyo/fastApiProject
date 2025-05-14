Важное:

Запуск redis:
sudo service redis-server start

Запуск celery( --pool=solo for windows):
celery -A app.tasks.celery_app:celery_app worker -l INFO --pool=solo

Запуск celery beat:
celery -A app.tasks.celery_app:celery_app beat -l INFO

Для тестов:

1) Создать файл .env-test с репликой базы

Флаги:
-v - надпись PASSED
-s - показывать print

pytest
