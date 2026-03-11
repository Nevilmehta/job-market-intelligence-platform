from datetime import date
from sqlalchemy.orm import Session
from app.models.analytics import JobDailyCount, TopCompany

class AnalyticsRepository:
    def __init__(self, db:Session):
        self.db = db

    def clear_job_daily_counts(self):
        self.db.query(JobDailyCount).delete()
        self.db.commit()

    def clear_top_companies(self):
        self.db.query(TopCompany).delete()
        self.db.commit()

    def create_job_daily_count(self, metric_date: date, job_count: int):
        row = JobDailyCount(metric_date=metric_date, job_count=job_count)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row 

    def create_top_company(self, company: str, job_count: int):
        row = TopCompany(company=company, job_count=job_count)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_job_daily_counts(self):
        return (self.db.query(JobDailyCount).order_by(JobDailyCount.metric_date.asc()).all())

    def get_top_companies(self):
        return (self.db.query(TopCompany).order_by(TopCompany.job_count.desc(), TopCompany.company.asc()).all())