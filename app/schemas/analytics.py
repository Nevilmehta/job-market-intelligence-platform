from datetime import date
from pydantic import BaseModel

# These schemas define analytics API responses.
class AnalyticsGenerationResponse(BaseModel):
    daily_metrics_created: int
    top_company_rows_created: int
    message: str

class JobDailyCountResponse(BaseModel):
    metric_date: date
    job_count: int

class JobDailyCountListResponse(BaseModel):
    items: list[JobDailyCountResponse]

class TopCompanyResponse(BaseModel):
    company: str
    job_count: int

class TopCompanyListResponse(BaseModel):
    items: list[TopCompanyResponse]