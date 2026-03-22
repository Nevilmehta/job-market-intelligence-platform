from app.core.database import SessionLocal
from app.services.validation_service import ValidationService
from app.tasks.celery_app import celery_app

@celery_app.task(bind=True, name="tasks.validate_raw_jobs", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def validate_raw_jobs_task(self):
    db= SessionLocal()
    try: 
        service = ValidationService(db)
        result = service.process_raw_jobs()
        return result
    finally:
        db.close()