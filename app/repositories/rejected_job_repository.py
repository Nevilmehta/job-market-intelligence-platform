from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.rejected_job import RejectedJob

# this repository stores invalid raw records
class RejectedJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_rejected_job(
        self, 
        source: str,
        external_id: str | None,
        payload: dict,
        error_reason: str
    ):
        rejected_job = RejectedJob(
            source=source,
            external_id=external_id,
            payload=payload,
            error_reason=error_reason,
        )

        self.db.add(rejected_job)
        self.db.commit()
        self.db.refresh(rejected_job)
        return rejected_job

    def count_all(self):
        return self.db.query(RejectedJob).count()

    def get_recent_rejected_jobs(self, limit: int=10):
        return (
            self.db.query(RejectedJob).order_by(RejectedJob.rejected_at.desc()).limit(limit).all()
        )

    def get_rejection_reason_counts(self):
        return (
            self.db.query(
                RejectedJob.error_reason, 
                func.count(RejectedJob.id)
            )
            .group_by(RejectedJob.error_reason)
            .order_by(func.count(RejectedJob.id).desc(), RejectedJob.error_reason.asc())
            .all()
        )