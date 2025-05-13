from time import sleep

from app.tasks.celery_app import celery_app


@celery_app.task
def test_task():
    sleep(6)
    print("Ну все типо")
