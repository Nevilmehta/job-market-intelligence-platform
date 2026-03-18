from sqlalchemy.orm import Session
from app.models.staging_job import StagingJob
from datetime import date, datetime

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
        salary_min: int | None,
        salary_max: int | None,
        salary_currency: str | None,
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
            salary_min=salary_min,
            salary_max=salary_max,
            salary_currency=salary_currency,
            technologies=technologies,
            posted_date=posted_date,
        )
        self.db.add(staging_job)
        self.db.commit()
        self.db.refresh(staging_job)
        return staging_job

    def get_all_staging_jobs(self):
        return (
            self.db.query(StagingJob).order_by(StagingJob.id.asc()).all()
        )

    def get_staging_jobs_in_date_range(self, date_from: date, date_to: date):
        rows = (
            self.db.query(StagingJob)
            .filter(StagingJob.posted_date.isnot(None))
            .order_by(StagingJob.id.asc())
            .all()
        )

        filtered_rows = []

        for row in rows:
            try: 
                parsed_date = datetime.strptime(row.posted_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue

            if date_from <= parsed_date <= date_to:
                filtered_rows.append(row)

        return filtered_rows