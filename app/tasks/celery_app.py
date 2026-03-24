from celery import Celery
from app.core.config import settings
from celery.schedules import crontab

celery_app = Celery(
    "job_market_tasks",
    broker = settings.CELERY_BROKER_URL,
    backend = settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.validation_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.backfill_tasks"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
    # name must match with the name u have used for task decorator
    beat_schedule={
        "validate-raw-jobs-every-10-minutes": {
            "task": "tasks.validate_raw_jobs",
            "schedule": crontab(minute="*/10")
        },
        "generate-core-analytics-nightly": {
            "task": "tasks.generate_core_analytics",
            "schedule": crontab(hour=2, minute=0)
        }
    }
)