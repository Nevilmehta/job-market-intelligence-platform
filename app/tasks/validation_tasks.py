from app.core.database import SessionLocal
from app.services.validation_service import ValidationService
from app.tasks.celery_app import celery_app

@celery_app.task(name="tasks.validate_raw_jobs")
def validate_raw_jobs_task():
    db= SessionLocal()
    try: 
        service = ValidationService(db)
        result = service.process_raw_jobs()
        return result
    finally:
        db.close()