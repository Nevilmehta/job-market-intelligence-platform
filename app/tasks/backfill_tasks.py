from app.core.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.tasks.celery_app import celery_app
from datetime import date

@celery_app.task(bind=True, name="tasks.backfill_analytics", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def backfill_analytics_task(date_from: str, date_to: str):

    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        result = service.backfill_analytics_for_date_range(
            date_from=date.fromisoformat(date_from),
            date_to=date.fromisoformat(date_to)
        )
        return result
    finally:
        db.close()