import pytest

from framework.api.auth_api import AuthAPI
from framework.env_manager import EnvManager


@pytest.fixture(scope="session")
def email_dev() -> str:
    return EnvManager.get("USER_EMAIL_DEV", required=True)


@pytest.fixture(scope="session")
def password_dev() -> str:
    return EnvManager.get("USER_PASSWORD_DEV", required=True)


@pytest.fixture(scope="session")
def email_admin() -> str:
    return EnvManager.get("ADMIN_USER_EMAIL", required=True)


@pytest.fixture(scope="session")
def password_admin() -> str:
    return EnvManager.get("ADMIN_USER_PASSWORD", required=True)


@pytest.fixture(scope="session")
def auth_tokens(email_dev: str, password_dev: str) -> dict:
    """
    Authenticates a regular user once per test session
    and returns the token dictionary.
    """
    auth_api = AuthAPI()
    response = auth_api.authorization(email=email_dev, password=password_dev)

    if response.status_code != 200:
        raise RuntimeError(
            f"Authentication failed for user '{email_dev}'. "
            f"Status: {response.status_code}, Body: {response.text}"
        )

    return response.json()


@pytest.fixture(scope="session")
def admin_tokens(email_admin: str, password_admin: str) -> dict:
    """
    Authenticates an admin user once per test session
    and returns the token dictionary.
    """
    auth_api = AuthAPI()
    response = auth_api.authorization(email=email_admin, password=password_admin)

    if response.status_code != 200:
        raise RuntimeError(
            f"Authentication failed for admin '{email_admin}'. "
            f"Status: {response.status_code}, Body: {response.text}"
        )

    return response.json()