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
            skill_counts = Counter()
            salary_buckets = defaultdict(list)

            for job in staging_jobs:

                parsed_date = None
                if job.posted_date:
                    try:
                        parsed_date = datetime.strptime(job.posted_date, "%Y-%m-%d").date()
                        daily_counts[parsed_date] += 1
                    except ValueError:
                        pass

                if job.company:
                    company_counts[job.company] += 1

                if job.technologies and isinstance(job.technologies, list):
                    normalized_skills_for_job = set()

                    for skill in job.technologies:
                        if isinstance(skill, str):
                            cleaned_skill = skill.strip()
                            if cleaned_skill:
                                normalized_skills_for_job.add(cleaned_skill)

                    for skill in normalized_skills_for_job:
                        skill_counts[skill]+= 1

                if parsed_date and job.salary_min is not None and job.salary_max is not None:
                    midpoint_salary = (job.salary_min + job.salary_max)//2
                    salary_buckets[(parsed_date, job.salary_currency)].append(midpoint_salary)

            self.analytics_repository.clear_job_daily_counts()
            self.analytics_repository.clear_top_companies()
            self.analytics_repository.clear_top_skills()
            self.analytics_repository.clear_salary_trends()

            daily_rows_created = 0
            top_company_rows_created = 0
            top_skill_rows_created = 0
            salary_trend_rows_created = 0

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

            for skill, count in skill_counts.most_common(15):
                self.analytics_repository.create_top_skill(
                    skill=skill,
                    demand_count=count
                )
                top_skill_rows_created += 1

            for (metric_date, currency), salaries in sorted(salary_buckets.items()):
                average_salary = sum(salaries)//len(salaries)

                self.analytics_repository.create_salary_trend(
                    metric_date=metric_date,
                    average_salary=average_salary,
                    currency=currency,
                    job_count=len(salaries)
                )
                salary_trend_rows_created+= 1

            total_rows_created = (daily_rows_created + top_company_rows_created + top_skill_rows_created + salary_trend_rows_created)

            self.etl_job_run_repository.complete_job_run(
                job_run=job_run,
                status="success",
                records_processed=total_rows_created,
                records_failed=0
            )

            return {
                "daily_metrics_created": daily_rows_created,
                "top_company_rows_created": top_company_rows_created,
                "top_skill_rows_created": top_skill_rows_created,
                "salary_trend_rows_created": salary_trend_rows_created,
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

    def get_top_skills(self):
        return self.analytics_repository.get_top_skills()

    def get_salary_trends(self):
        return self.analytics_repository.get_salary_trends()