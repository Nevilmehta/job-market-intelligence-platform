from app.core.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.tasks.celery_app import celery_app
from datetime import date

@celery_app.task(name="tasks.backfill_analytics")
def backfill_analytics_task(date_from: str, date_to: str):
    from datetime import date

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