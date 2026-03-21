from app.core.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.tasks.celery_app import celery_app

@celery_app.task(name="tasks.generate_core_analytics")
def generate_core_analytics_task():
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        result = service.generate_core_analytics()
        return result
    finally:
        db.close()