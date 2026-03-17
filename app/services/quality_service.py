from sqlalchemy.orm import Session
from app.repositories.raw_job_repository import RawJobRepository
from app.repositories.rejected_job_repository import RejectedJobRepository

class QualityService:
    def __init__(self, db: Session):
        self.db = db
        self.raw_job_repository = RawJobRepository(db)
        self.rejected_job_repository = RejectedJobRepository(db)

    def get_quality_summary(self):
        total_raw_jobs = self.raw_job_repository.count_all()
        processed_raw_jobs = self.raw_job_repository.count_processed()
        unprocessed_raw_jobs = self.raw_job_repository.count_unprocessed()
        total_rejected_jobs = self.rejected_job_repository.count_all()

        processing_rate_percent = 0.0
        if total_raw_jobs>0:
            processing_rate_percent = round((processed_raw_jobs/total_raw_jobs)*100, 2)

        return {
            "total_raw_jobs": total_raw_jobs,
            "processed_raw_jobs": processed_raw_jobs,
            "unprocessed_raw_jobs": unprocessed_raw_jobs,
            "total_rejected_jobs": total_rejected_jobs,
            "processing_rate_percent": processing_rate_percent
        }

    def get_rejection_reason_breakdown(self):
        rows = self.rejected_job_repository.get_rejection_reason_counts()

        return [
            {
                "error_reason": error_reason,
                "count": count
            }
            for error_reason, count in rows
        ]

    def get_recent_rejected_jobs(self, limit: int=10):
        return self.rejected_job_repository.get_recent_rejected_jobs(limit=limit)