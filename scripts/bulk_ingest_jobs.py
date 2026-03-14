import json
import requests

API_URL = "http://127.0.0.1:8000/v1/ingest/jobs"
DATA_FILE = "scripts/sample_jobs.json"


def ingest_jobs():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    success_count = 0
    failed_count = 0

    for job in jobs:
        try:
            response = requests.post(API_URL, json=job, timeout=10)

            if response.status_code == 201:
                success_count += 1
                print(f"SUCCESS: {job['external_id']} ingested")
            else:
                failed_count += 1
                print(f"FAILED: {job['external_id']} | Status: {response.status_code} | Response: {response.text}")

        except requests.RequestException as exc:
            failed_count += 1
            print(f"ERROR: {job['external_id']} | Exception: {exc}")

    print("\nBulk ingestion completed")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")


if __name__ == "__main__":
    ingest_jobs()
