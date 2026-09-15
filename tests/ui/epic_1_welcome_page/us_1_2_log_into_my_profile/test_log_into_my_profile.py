import allure
import pytest

from framework.env_manager import EnvManager
from framework.ui.pages.log_into_my_profile import SignInPage
from tests.ui.epic_1_welcome_page.data.log_into_my_profile_data import (
    INVALID_SIGN_IN_DATA,
    VALID_SIGN_IN_DATA,
    VALIDATION_SIGN_IN_DATA,
)

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@allure.parent_suite("UI Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.2 Log Into My Profile")
class _SignInBase:
    """Shared Allure hierarchy for all sign-in UI test classes."""

    def _open_login_page(self, page) -> SignInPage:
        sign_in = SignInPage(page)
        base_url = EnvManager.get_config().base_url
        page.goto(base_url)
        sign_in.open_sign_in_page()
        sign_in.expect_url_is_login(base_url)
        return sign_in


@allure.story("Successful login")
@pytest.mark.qase("LP-121")
class TestSuccessfulLogin(_SignInBase):
    test_data_map = {"sign_in_case": VALID_SIGN_IN_DATA}

    @allure.title("Successful login with valid credentials — {sign_in_case}")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, page, sign_in_case):
        base_url = EnvManager.get_config().base_url
        sign_in = self._open_login_page(page)

        with allure.step(f"Fill email: {sign_in_case['email']!r}"):
            sign_in.fill_email(sign_in_case["email"])
        with allure.step("Fill password"):
            sign_in.fill_password(sign_in_case["password"])
        with allure.step("Assert login button is enabled"):
            sign_in.expect_login_button_enabled()
        with allure.step("Click login button"):
            sign_in.click_login()
        with allure.step("Assert redirected away from login page"):
            sign_in.expect_url_is_not_login(base_url)


@allure.story("Field validation errors")
@pytest.mark.qase("LP-122")
class TestFieldValidationErrors(_SignInBase):

    @allure.title("Email validation error is shown after clearing email field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_email_error_after_clearing_field(self, page):
        sign_in = self._open_login_page(page)

        with allure.step("Fill email then clear it"):
            sign_in.fill_email("test@email.com")
            sign_in.clear_email()
            sign_in.click_password_field()
        with allure.step("Assert validation error is shown"):
            sign_in.expect_validation_error_contains("Email address is required")
        with allure.step("Assert login button is disabled"):
            sign_in.expect_login_button_disabled()

    @allure.title("Password validation error is shown after clearing password field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password_error_after_clearing_field(self, page):
        sign_in = self._open_login_page(page)

        with allure.step("Fill password then clear it"):
            sign_in.fill_email("test@email.com")
            sign_in.fill_password("Test@1234!")
            sign_in.clear_password()
            sign_in.click_email_field()
        with allure.step("Assert validation error is shown"):
            sign_in.expect_validation_error_contains("Password is required")
        with allure.step("Assert login button is disabled"):
            sign_in.expect_login_button_disabled()


@allure.story("UI input validation")
@pytest.mark.qase("LP-123")
class TestInputValidation(_SignInBase):
    test_data_map = {"sign_in_case": VALIDATION_SIGN_IN_DATA}

    @allure.title("Login button disabled and validation error shown for invalid email — {sign_in_case}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validation_errors_for_invalid_ui_data(self, page, sign_in_case):
        sign_in = self._open_login_page(page)

        with allure.step(f"Fill email: {sign_in_case['email']!r}"):
            sign_in.fill_email(sign_in_case["email"])
        with allure.step("Fill password"):
            sign_in.fill_password(sign_in_case["password"])
            sign_in.click_password_field()
        with allure.step("Assert login button is disabled"):
            sign_in.expect_login_button_disabled()
        with allure.step(f"Assert validation error: {sign_in_case['expected_error']!r}"):
            sign_in.expect_validation_error_contains(sign_in_case["expected_error"])


@allure.story("Invalid credentials error")
@pytest.mark.qase("LP-124")
class TestInvalidCredentials(_SignInBase):
    test_data_map = {"sign_in_case": INVALID_SIGN_IN_DATA}

    @allure.title("Error message shown for invalid credentials — {sign_in_case}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_login_credentials(self, page, sign_in_case):
        base_url = EnvManager.get_config().base_url
        sign_in = self._open_login_page(page)

        with allure.step(f"Fill email: {sign_in_case['email']!r}"):
            sign_in.fill_email(sign_in_case["email"])
        with allure.step("Fill password"):
            sign_in.fill_password(sign_in_case["password"])
        with allure.step("Assert login button is enabled before submit"):
            sign_in.expect_login_button_enabled()
        with allure.step("Click login button"):
            sign_in.click_login()
        with allure.step(f"Assert error: {sign_in_case['expected_error']!r}"):
            sign_in.expect_general_error_contains(sign_in_case["expected_error"])
        with allure.step("Assert still on login page"):
            sign_in.expect_url_is_login(base_url)


@allure.story("Account lockout")
@pytest.mark.qase("LP-125")
class TestAccountLockout(_SignInBase):

    @allure.title("User is blocked for 15 minutes after 5 failed login attempts")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Account lock after 5 failed attempts is not implemented yet")
    def test_user_blocked_after_5_failed_login_attempts(self, page):
        base_url = EnvManager.get_config().base_url
        sign_in = self._open_login_page(page)

        email = "xonib78658@inreur.com"
        wrong_password = "WrongPass123!"
        expected_error = "Incorrect email or password"
        expected_block_message = "Your account is temporarily locked"

        for attempt in range(5):
            with allure.step(f"Login attempt {attempt + 1} with wrong password"):
                sign_in.fill_email(email)
                sign_in.fill_password(wrong_password)
                sign_in.expect_login_button_enabled()
                sign_in.click_login()
                if attempt < 4:
                    sign_in.expect_general_error_contains(expected_error)

        with allure.step("Assert account is locked after 5 attempts"):
            sign_in.expect_general_error_contains(expected_block_message)
            sign_in.expect_url_is_login(base_url)
