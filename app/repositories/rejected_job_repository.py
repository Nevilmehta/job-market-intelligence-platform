from sqlalchemy.orm import Session
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