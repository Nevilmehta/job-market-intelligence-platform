from sqlalchemy.orm import Session
from app.models.staging_job import StagingJob

# this repository saves validated records
class StagingJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_staging_job(
        self, 
        source: str,
        external_id: str,
        title: str,
        company: str,
        location: str | None,
        salary_text: str | None,
        technologies: list[str] | None,
        posted_date: str | None
    ):
        staging_job = StagingJob(
            source=source,
            external_id=external_id,
            title=title,
            company=company,
            location=location,
            salary_text=salary_text,
            technologies=technologies,
            posted_date=posted_date,
        )
        self.db.add(staging_job)
        self.db.commit()
        self.db.refresh(staging_job)
        return staging_job