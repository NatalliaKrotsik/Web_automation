import allure
import pytest
from assertpy import assert_that

from tests.api.epic_1_welcome_page.data.log_into_my_profile_data import (
    INVALID_SIGN_IN_DATA,
    VALID_SIGN_IN_DATA,
)

pytestmark = [pytest.mark.api, pytest.mark.regression]


@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.2 Log Into My Profile")
class _SignInBase:
    """Shared Allure hierarchy for all sign-in test classes."""


@allure.story("Check sign-in process with valid data")
@pytest.mark.qase("LP-164")
class TestValidSignIn(_SignInBase):
    @pytest.mark.parametrize("sign_in_case", VALID_SIGN_IN_DATA, ids=lambda c: c["name"])
    @allure.title("Sign in with valid credentials — {sign_in_case[name]}")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_sign_in_with_valid_credentials(self, auth_api, sign_in_case):
        with allure.step(f"POST sign-in with email={sign_in_case['email']!r}"):
            response = auth_api.sign_in(
                email=sign_in_case["email"],
                password=sign_in_case["password"],
            )
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as("Expected 200 for valid credentials").is_equal_to(
                sign_in_case["expected_status"]
            )
        with allure.step("Assert response contains auth tokens"):
            body = response.json()
            assert_that(body).described_as("Response body must not be empty").is_not_none()
            assert_that(body.get("authenticationResult")).described_as(
                "Response must contain authenticationResult"
            ).is_not_none()


@allure.story("Check sign-in process with invalid data")
@pytest.mark.qase("LP-171")
class TestInvalidSignIn(_SignInBase):
    @pytest.mark.parametrize("sign_in_case", INVALID_SIGN_IN_DATA, ids=lambda c: c["name"])
    @allure.title("Sign in with invalid credentials — {sign_in_case[name]}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sign_in_with_invalid_credentials(self, auth_api, sign_in_case):
        with allure.step(f"POST sign-in with email={sign_in_case['email']!r}"):
            response = auth_api.sign_in(
                email=sign_in_case["email"],
                password=sign_in_case["password"],
            )
        with allure.step(f"Assert status code is {sign_in_case['expected_status']}"):
            assert_that(response.status_code).described_as(
                f"Expected {sign_in_case['expected_status']} for case {sign_in_case['name']!r}"
            ).is_equal_to(sign_in_case["expected_status"])
        with allure.step("Assert error message is present in response"):
            if sign_in_case["expected_error"]:
                assert_that(response.text).described_as("Response must contain expected error message").contains(
                    sign_in_case["expected_error"]
                )
