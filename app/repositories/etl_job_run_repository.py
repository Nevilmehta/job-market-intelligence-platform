from datetime import datetime, UTC
from sqlalchemy.orm import Session
from app.models.etl_job_run import ETLJobRun

class ETLJobRunRepository:
    def __init__(self, db:Session):
        self.db = db

    def create_job_run(self, job_name: str, status: str = "running"):
        job_run =ETLJobRun(
            job_name = job_name,
            status = status,
            records_processed=0,
            records_failed=0,
        )
        self.db.add(job_run)
        self.db.commit()
        self.db.refresh(job_run)
        return job_run

    def complete_job_run(self, job_run: ETLJobRun, status: str, records_processed: int, records_failed: int, error_message: str|None = None):
        job_run.status = status
        job_run.records_processed = records_processed
        job_run.records_failed = records_failed
        job_run.error_message = error_message
        job_run.ended_at = datetime.now(UTC)

        self.db.commit()
        self.db.refresh(job_run)
        return job_run

    def get_all_job_runs(self):
        return(
            self.db.query(ETLJobRun)
            .order_by(ETLJobRun.started_at.desc())
            .all()
        )

    def get_job_run_by_id(self, run_id: int):
        return(
            self.db.query(ETLJobRun)
            .filter(ETLJobRun.id == run_id)
            .first()
        )