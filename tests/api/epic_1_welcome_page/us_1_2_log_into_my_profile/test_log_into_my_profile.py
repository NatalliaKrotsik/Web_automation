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


@allure.story("Valid credentials")
@pytest.mark.qase("LP-121")
class TestValidSignIn(_SignInBase):
    test_data_map = {"sign_in_case": VALID_SIGN_IN_DATA}

    @allure.title("Sign in with valid credentials — {sign_in_case}")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_sign_in_with_valid_credentials(self, auth_api, sign_in_case):
        with allure.step(f"POST sign-in with email={sign_in_case['email']!r}"):
            response = auth_api.sign_in(
                email=sign_in_case["email"],
                password=sign_in_case["password"],
            )
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as(
                "Expected 200 for valid credentials"
            ).is_equal_to(sign_in_case["expected_status"])
        with allure.step("Assert response contains auth tokens"):
            body = response.json()
            assert_that(body).described_as("Response body must not be empty").is_not_none()
            assert_that(body.get("authenticationResult")).described_as(
                "Response must contain authenticationResult"
            ).is_not_none()


@allure.story("Invalid credentials")
@pytest.mark.qase("LP-122")
class TestInvalidSignIn(_SignInBase):
    test_data_map = {"sign_in_case": INVALID_SIGN_IN_DATA}

    @allure.title("Sign in with invalid credentials — {sign_in_case}")
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
                assert_that(response.text).described_as(
                    "Response must contain expected error message"
                ).contains(sign_in_case["expected_error"])


@allure.story("Account lockout")
@pytest.mark.qase("LP-123")
class TestAccountLockout(_SignInBase):

    @allure.title("User is blocked after 5 consecutive invalid sign-in attempts")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_is_blocked_after_5_invalid_attempts(self, auth_api):
        blocked_email = "xonib78658@inreur.com"
        wrong_password = "wrong_password"
        correct_password = "Aa12345!"

        with allure.step("Send 5 invalid sign-in attempts"):
            for attempt in range(1, 6):
                with allure.step(f"Attempt {attempt} with wrong password"):
                    response = auth_api.sign_in(email=blocked_email, password=wrong_password)
                    assert_that(response.status_code).described_as(
                        f"Attempt {attempt}: expected 401 Unauthorized"
                    ).is_equal_to(401)

        with allure.step("Sign in with correct password — account should be locked"):
            response = auth_api.sign_in(email=blocked_email, password=correct_password)
            assert_that(response.status_code).described_as(
                "Account must be locked (423) after 5 failed attempts"
            ).is_equal_to(423)
