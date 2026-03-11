from collections import Counter, defaultdict
from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.etl_job_run_repository import ETLJobRunRepository
from app.repositories.staging_job_repository import StagingJobRepository

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.analytics_repository = AnalyticsRepository(db)
        self.staging_job_repository = StagingJobRepository(db)
        self.etl_job_run_repository = ETLJobRunRepository(db)

    def generate_core_analytics(self):
        job_run = self.etl_job_run_repository.create_job_run(
            job_name="generate_core_analytics",
            status="running"
        )

        try:
            staging_jobs = self.staging_job_repository.get_all_staging_jobs()

            daily_counts = defaultdict(int)
            company_counts = Counter()

            for job in staging_jobs:
                if job.posted_date:
                    try:
                        posted_date = datetime.strptime(job.posted_date, "%Y-%m-%d").date()
                        daily_counts[parsed_date] += 1
                    except ValueError:
                        pass

                if job.company:
                    company_counts[job.company] += 1

            self.analytics_repository.clear_job_daily_counts()
            self.analytics_repository.clear_top_companies()

            daily_rows_created = 0
            top_company_rows_created = 0

            for metric_date, count in sorted(daily_counts.items()):
                self.analytics_repository.create_job_daily_count(
                    metric_date=metric_date,
                    job_count=count
                )
                daily_rows_created += 1

            for company, count in company_counts.most_common(10):
                self.analytics_repository.create_top_company(
                    company=company,
                    job_count=count
                )
                top_company_rows_created += 1

            total_rows_created = daily_rows_created + top_company_rows_created

            self.etl_job_run_repository.complete_job_run(
                job_run=job_run,
                status="success",
                records_processed=total_rows_created,
                records_failed=0
            )

            return {
                "daily_metrics_created": daily_rows_created,
                "top_company_rows_created": top_company_rows_created,
                "message": "Core Analytics generated successfully"
            }

        except Exception as exc:
            self.etl_job_run_repository.complete_job_run(
                job_run= job_run,
                status= "failed",
                records_failed= 0,
                records_processed= 0,
                error_message=str(exc)
            )
            raise

    def get_job_daily_counts(self):
        return self.analytics_repository.get_job_daily_counts()

    def get_top_companies(self):
        return self.analytics_repository.get_top_companies()