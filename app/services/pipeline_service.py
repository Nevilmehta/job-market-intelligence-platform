from sqlalchemy.orm import Session
from app.repositories.etl_job_run_repository import ETLJobRunRepository

# the service will handle pipeline history queries
class PipelineService:
    def __init__(self, db: Session):
        self.db = db
        self.etl_job_run_repository = ETLJobRunRepository(db)

    def list_pipeline_runs(self):
        return self.etl_job_run_repository.get_all_job_runs()

    def get_pipeline_run(self, run_id: int):
        return self.etl_job_run_repository.get_job_run_by_id(run_id)