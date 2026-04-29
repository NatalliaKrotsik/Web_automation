import pytest

def get_valid_user() -> dict:
    return {"email": "jan.kowalski.test@mailinator.com", "password": "Test@1234!"}

INVALID_PASSWORD = pytest.param(
    {"email": "jan.kowalski.test@mailinator.com", "password": "WrongPass!99"},
    id="invalid_password",
)

INVALID_EMAIL_FORMAT = pytest.param(
    {"email": "not-an-email", "password": "Test@1234!"},
    id="invalid_email_format",
)

EMPTY_EMAIL = pytest.param(
    {"email": "", "password": "Test@1234!"},
    id="empty_email",
)

EMPTY_PASSWORD = pytest.param(
    {"email": "jan.kowalski.test@mailinator.com", "password": ""},
    id="empty_password",
)

BOTH_FIELDS_EMPTY = pytest.param(
    {"email": "", "password": ""},
    id="both_fields_empty",
)