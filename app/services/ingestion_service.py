from sqlalchemy.orm import Session
from app.repositories.raw_job_repository import RawJobRepository
from app.schemas.ingestion import JobIngestionRequest
from app.core.exceptions import DuplicateRawJobException

# This is the business logic layer
class IngestionService:
    def __init__(self, db:Session):
        self.db=db
        self.raw_job_repository=RawJobRepository(db)

    # duplicate logic
    def ingest_job(self, request: JobIngestionRequest):
        existing_raw_job = self.raw_job_repository.get_by_source_and_external_id(
            source=request.source,
            external_id=request.external_id
        )

        if existing_raw_job:
            raise DuplicateRawJobException(
                f"Job with source='{request.source}' and external_id='{request.external_id}' already exists."
            )

        raw_job = self.raw_job_repository.create_raw_job(
            source=request.source,
            external_id=request.external_id,
            payload=request.payload
        )
        return raw_job