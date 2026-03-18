from sqlalchemy.orm import Session
from datetime import date
from app.repositories.etl_job_run_repository import ETLJobRunRepository
from app.services.analytics_service import AnalyticsService

# the service will handle pipeline history queries
class PipelineService:
    def __init__(self, db: Session):
        self.db = db
        self.etl_job_run_repository = ETLJobRunRepository(db)
        self.analytics_service = AnalyticsService(db)

    def list_pipeline_runs(self):
        return self.etl_job_run_repository.get_all_job_runs()

    def get_pipeline_run(self, run_id: int):
        return self.etl_job_run_repository.get_job_run_by_id(run_id)

    def backfill_analytics(self, date_from: date, date_to: date):
        return self.analytics_service.backfill_analytics_for_date_range(
            date_from=date_from,
            date_to=date_to
        )