from sqlalchemy.orm import Session
from app.models.raw_job import RawJob
from datetime import datetime, UTC

# this file talk directly to the database
class RawJobRepository:
    def __init__(self, db:Session):
        self.db = db

    # We add a lookup method.
    def get_by_source_and_external_id(self, source: str, external_id: str):
        return(
            self.db.query(RawJob).filter(RawJob.source == source, RawJob.external_id==external_id).first()
        )

    def create_raw_job(self, source: str, external_id: str, payload: dict):
        raw_job = RawJob(
            source=source,
            external_id=external_id,
            payload=payload,
        )
        self.db.add(raw_job)
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job

    # fetching only unprocessed raw jobs
    def get_unprocessed_raw_jobs(self):
        return (
            self.db.query(RawJob)
            .filter(RawJob.is_processed.is_(False))
            .order_by(RawJob.id.asc())
            .all()
        )

    # marking a raw job as processed
    def mark_as_processed(self, raw_job: RawJob):
        raw_job.is_processed = True
        raw_job.processed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job

    # we need methods to fetch raw jobs for validation
    # def get_all_raw_jobs(self):
    #     return self.db.query(RawJob).order_by(RawJob.id.asc()).all()