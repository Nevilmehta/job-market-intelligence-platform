import re
from sqlalchemy.orm import Session
from app.repositories.raw_job_repository import RawJobRepository
from app.repositories.rejected_job_repository import RejectedJobRepository
from app.repositories.staging_job_repository import StagingJobRepository
from app.repositories.etl_job_run_repository import ETLJobRunRepository

# this is the heart of the step
# read raw jobs, validate required fields, write valid records to staging, write invalid records to rejected

class ValidationService:
    def __init__(self, db:Session):
        self.db=db
        self.raw_job_repository=RawJobRepository(db)
        self.staging_job_repository=StagingJobRepository(db)
        self.rejected_job_repository=RejectedJobRepository(db)
        self.etl_job_run_repository=ETLJobRunRepository(db)

    def _validate_payload(self, payload:dict):
        required_fields = ["title", "company"]

        for field in required_fields:
            value = payload.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                return False, f"Missing or empty required field: {field}"

        return True, None

    def _parse_salary(self, salary_text: str|None):
        if not salary_text or not isinstance(salary_text, str):
            return None, None, None

        currency=None
        if "£" in salary_text:
            currency = "GBP"
        elif "$" in salary_text:
            currency = "USD"
        elif "€" in salary_text:
            currency = "EUR"

        numbers = re.findall(r"\d[\d,]*", salary_text)
        parsed_numbers = []

        for num in numbers:
            cleaned = num.replace(",", "")
            if cleaned.isdigit():
                parsed_numbers.append(int(cleaned))

        if not parsed_numbers:
            return None, None, currency

        if len(parsed_numbers)==1:
            return parsed_numbers[0], parsed_numbers[0], currency

        return min(parsed_numbers), max(parsed_numbers), currency

    # Now we wrap pipeline execution with job tracking.
    # Now we process only unprocessed records and mark them after handling. P6
    def process_raw_jobs(self):

        job_run = self.etl_job_run_repository.create_job_run(
            job_name = "validate_raw_jobs",
            status = "running",
        )

        valid_records = 0
        rejected_records = 0

        try:
            raw_jobs = self.raw_job_repository.get_unprocessed_raw_jobs()
            total_records = len(raw_jobs)

            for raw_job in raw_jobs:
                payload = raw_job.payload
                is_valid, error_reason = self._validate_payload(payload)

                if not is_valid:
                    self.rejected_job_repository.create_rejected_job(
                        source=raw_job.source,
                        external_id=raw_job.external_id,
                        payload=payload,
                        error_reason=error_reason or "Unknown validation error"
                    )
                    self.raw_job_repository.mark_as_processed(raw_job)
                    rejected_records += 1
                    continue

                salary_text = payload.get("salary")
                salary_min, salary_max, salary_currency = self._parse_salary(salary_text)
                
                self.staging_job_repository.create_staging_job(
                    source=raw_job.source,
                    external_id=raw_job.external_id,
                    title=payload.get("title"),
                    company=payload.get("company"),
                    location=payload.get("location"),
                    salary_text=salary_text,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_currency=salary_currency,
                    technologies=payload.get("technologies"),
                    posted_date=payload.get("posted_date")
                )
                self.raw_job_repository.mark_as_processed(raw_job)
                valid_records += 1

            self.etl_job_run_repository.complete_job_run(
                job_run = job_run,
                status = "success",
                records_processed = valid_records,
                records_failed = rejected_records
            )

            return {
                "total_records": total_records,
                "valid_records": valid_records,
                "rejected_records": rejected_records,
                "message": "Validation Pipeline completed successfully"
            }

        except Exception as exc:
            self.etl_job_run_repository.complete_job_run(
                job_run=job_run,
                status="failed",
                records_processed=valid_records,
                records_failed=rejected_records,
                error_message=str(exc)
            )
            raise