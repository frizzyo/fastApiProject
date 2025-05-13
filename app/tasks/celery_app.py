from celery import Celery

from app.config import settings


celery_app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['app.tasks.tasks',]
)

celery_app.conf.beat_schedule = {
    "name": {
        "task": "booking_today_checkin",
        "schedule": 5
    }
}
