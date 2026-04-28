import allure
import pytest
import yaml
from assertpy import assert_that
from framework.api.auth_api import AuthAPI


@pytest.mark.api
@allure.suite("API Tests - Auth")
class TestAuth:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login with invalid credentials should fail")
    def test_login_with_invalid_credentials(self):
        with open("tests/api/data/test_auth_data.yaml") as f:
            data = yaml.safe_load(f)
        credentials = data["invalid_credentials"][0]

        auth_api = AuthAPI()
        with pytest.raises(ValueError, match="Authorization failed"):
            auth_api.authorization(
                email=credentials["email"],
                password=credentials["password"]
            )