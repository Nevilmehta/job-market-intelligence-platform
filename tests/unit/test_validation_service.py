from app.services.validation_service import ValidationService

def make_service():
    return ValidationService(db=None)

def test_validate_payload_accepts_valid_payload():
    service = make_service()

    payload = {
        "title": "Backend Engineer",
        "company": "Acme Corp",
    }

    is_valid, error = service._validate_payload(payload)

    assert is_valid is True
    assert error is None


def test_validate_payload_rejects_missing_title():
    service = make_service()

    payload = {
        "company": "Acme Corp",
    }

    is_valid, error = service._validate_payload(payload)

    assert is_valid is False
    assert error == "Missing or empty required field: title"


def test_validate_payload_rejects_empty_company():
    service = make_service()

    payload = {
        "title": "Backend Engineer",
        "company": "   ",
    }

    is_valid, error = service._validate_payload(payload)

    assert is_valid is False
    assert error == "Missing or empty required field: company"


def test_parse_salary_returns_none_for_missing_salary():
    service = make_service()

    salary_min, salary_max, currency = service._parse_salary(None)

    assert salary_min is None
    assert salary_max is None
    assert currency is None


def test_parse_salary_parses_gbp_range():
    service = make_service()

    salary_min, salary_max, currency = service._parse_salary("£70,000 - £90,000")

    assert salary_min == 70000
    assert salary_max == 90000
    assert currency == "GBP"


def test_parse_salary_parses_single_value():
    service = make_service()

    salary_min, salary_max, currency = service._parse_salary("$120000")

    assert salary_min == 120000
    assert salary_max == 120000
    assert currency == "USD"


def test_parse_salary_returns_currency_even_if_numbers_missing():
    service = make_service()

    salary_min, salary_max, currency = service._parse_salary("£ negotiable")

    assert salary_min is None
    assert salary_max is None
    assert currency == "GBP"