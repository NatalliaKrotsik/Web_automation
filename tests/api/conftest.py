from typing import Dict
from assertpy import assert_that
import pytest
import os

from framework.api.auth_api import AuthAPI


@pytest.fixture
def email_dev() -> str:
    return os.getenv("USER_EMAIL_DEV")


@pytest.fixture
def password_dev() -> str:
    return os.getenv("USER_PASSWORD_DEV")


@pytest.fixture
def get_tokens(email_dev, password_dev) -> Dict:
    """Retrieves tokens from the Auth API."""
    auth_api = AuthAPI()
    tokens = auth_api.authorization(email=email_dev, password=password_dev)
    assert_that(tokens.status_code, "Sign in error.").is_equal_to(200)
    return tokens.json()


@pytest.fixture
def email_admin() -> str:
    return os.getenv("ADMIN_USER_EMAIL")


@pytest.fixture
def password_admin() -> str:
    return os.getenv("ADMIN_USER_PASSWORD")