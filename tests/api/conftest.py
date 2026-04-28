from typing import Dict
import pytest

from framework.api.auth_api import AuthAPI
from framework.env_manager import EnvManager


@pytest.fixture(scope="session")
def auth_tokens() -> Dict:
    """Retrieves authentication tokens from the Auth API."""
    auth_api = AuthAPI()
    tokens = auth_api.authorization(
        email=EnvManager.get("USER_EMAIL_DEV"),
        password=EnvManager.get("USER_PASSWORD_DEV")
    )
    return tokens.json()


@pytest.fixture(scope="session")
def admin_auth_tokens() -> Dict:
    """Retrieves admin authentication tokens from the Auth API."""
    auth_api = AuthAPI()
    tokens = auth_api.authorization(
        email=EnvManager.get("ADMIN_USER_EMAIL"),
        password=EnvManager.get("ADMIN_USER_PASSWORD")
    )
    return tokens.json()
