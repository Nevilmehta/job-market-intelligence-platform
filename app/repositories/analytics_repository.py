from datetime import date
from sqlalchemy.orm import Session
from app.models.analytics import JobDailyCount, TopCompany, TopSkill, SalaryTrend

class AnalyticsRepository:
    def __init__(self, db:Session):
        self.db = db

    def clear_job_daily_counts(self):
        self.db.query(JobDailyCount).delete()
        self.db.commit()

    def clear_top_companies(self):
        self.db.query(TopCompany).delete()
        self.db.commit()

    def clear_top_skills(self):
        self.db.query(TopSkill).delete()
        self.db.commit()

    def clear_salary_trends(self):
        self.db.query(SalaryTrend).delete()
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

    def create_top_skill(self, skill: str, demand_count: int) -> TopSkill:
        row = TopSkill(
            skill=skill,
            demand_count=demand_count,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def create_salary_trend(self, metric_date: date, average_salary: int, currency: str|None, job_count: int):
        row = SalaryTrend(
            metric_date=metric_date,
            average_salary=average_salary,
            currency=currency,
            job_count=job_count
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_job_daily_counts(self, date_from: date|None=None, date_to: date|None=None):
        query = self.db.query(JobDailyCount)
        if date_from:
            query = query.filter(JobDailyCount.metric_date>=date_from)
        if date_to:
            query = query.filter(JobDailyCount.metric_date<=date_to)

        return query.order_by(JobDailyCount.metric_date.asc()).all()

    def get_top_companies(self):
        return (self.db.query(TopCompany).order_by(TopCompany.job_count.desc(), TopCompany.company.asc()).all())

    def get_top_skills(self):
        return (self.db.query(TopSkill).order_by(TopSkill.demand_count.desc(), TopSkill.skill.asc()).all())

    def get_salary_trends(self, date_from: date|None=None, date_to: date|None=None):
        query = self.db.query(SalaryTrend)
        if date_from:
            query = query.filter(SalaryTrend.metric_date>=date_from)
        if date_to:
            query = query.filter(SalaryTrend.metric_date<=date_to)

        return query.order_by(SalaryTrend.metric_date.asc()).all()