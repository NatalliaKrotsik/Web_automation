import allure
import pytest
import yaml
from assertpy import assert_that
from framework.api.auth_api import AuthAPI


@pytest.mark.api
@allure.suite("API Tests - Auth")
class TestAuth:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login with valid credentials should succeed")
    def test_login_with_valid_credentials(self, auth_tokens):
        assert_that(auth_tokens).contains_key("authenticationResult")
        auth_result = auth_tokens.get("authenticationResult", {})
        assert_that(auth_result).contains_key("accessToken")
        assert_that(auth_result).contains_key("refreshToken")
        assert_that(auth_result.get("accessToken")).is_not_none()
        assert_that(auth_result.get("refreshToken")).is_not_none()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Logout should succeed")
    def test_logout(self, auth_tokens):
        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        auth_api = AuthAPI()
        auth_api.update_headers({"Authorization": f"Bearer {access_token}"})
        logout_response = auth_api.sign_out_user(access_token)
        assert_that(logout_response.status_code).is_equal_to(200)

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