from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import RawJob, RejectedJob, ETLJobRun, StagingJob, TopCompany, JobDailyCount

app = FastAPI(
    title = settings.APP_NAME,
    description = "A Backend platform for ingesting, preocessing and analyzing job market data",
    version = settings.APP_VERSION
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/", tags= ["Root"])
def root():
    return{
        "message": "welcome to the {settings.APP_NAME} API"
    }