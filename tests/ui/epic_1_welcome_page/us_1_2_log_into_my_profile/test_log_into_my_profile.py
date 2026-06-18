import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.log_into_my_profile import SignInLocators
from tests.ui.epic_1_welcome_page.data.log_into_my_profile_data import (
    INVALID_SIGN_IN_DATA,
    VALID_SIGN_IN_DATA,
    VALIDATION_SIGN_IN_DATA,
)

BASE_URL = "https://dev.pretty-py.andersenlab.dev"


@allure.epic("UI")
@allure.feature("Log into my profile")
class TestLogIntoMyProfile:

    def open_login_page(self, page):
        page.goto(BASE_URL)
        page.locator(SignInLocators.LOGIN_NAV_BUTTON).click()
        expect(page).to_have_url(f"{BASE_URL}/login")

    @allure.title("Successful login with valid credentials")
    @pytest.mark.parametrize("email, password", VALID_SIGN_IN_DATA)
    def test_successful_login(self, page, email, password):
        self.open_login_page(page)

        page.locator(SignInLocators.EMAIL_INPUT).fill(email)
        page.locator(SignInLocators.PASSWORD_INPUT).fill(password)

        expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_enabled()

        page.locator(SignInLocators.LOGIN_BUTTON).click()

        expect(page).not_to_have_url(f"{BASE_URL}/login")

    @allure.title("Email validation error is shown after clearing email field")
    def test_empty_email_error_after_clearing_field(self, page):
        self.open_login_page(page)

        page.locator(SignInLocators.EMAIL_INPUT).fill("test@email.com")
        page.locator(SignInLocators.EMAIL_INPUT).fill("")
        page.locator(SignInLocators.PASSWORD_INPUT).click()

        expect(page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text("Must be between 6 and 55 characters")
        expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()

    @allure.title("Password validation error is shown after clearing password field")
    def test_empty_password_error_after_clearing_field(self, page):
        self.open_login_page(page)

        page.locator(SignInLocators.EMAIL_INPUT).fill("test@email.com")
        page.locator(SignInLocators.PASSWORD_INPUT).fill("Test@1234!")
        page.locator(SignInLocators.PASSWORD_INPUT).fill("")
        page.locator(SignInLocators.EMAIL_INPUT).click()

        expect(page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text("Password is required")
        expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()

    @allure.title("Login button is disabled and validation error is shown for invalid email data")
    @pytest.mark.parametrize("email, password, expected_error", VALIDATION_SIGN_IN_DATA)
    def test_validation_errors_for_invalid_ui_data(self, page, email, password, expected_error):
        self.open_login_page(page)

        page.locator(SignInLocators.EMAIL_INPUT).fill(email)
        page.locator(SignInLocators.PASSWORD_INPUT).fill(password)
        page.locator(SignInLocators.PASSWORD_INPUT).click()

        expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()
        expect(page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text(expected_error)

    @allure.title("Error message is shown for invalid credentials")
    @pytest.mark.parametrize("email, password, expected_error", INVALID_SIGN_IN_DATA)
    def test_invalid_login_credentials(self, page, email, password, expected_error):
        self.open_login_page(page)

        page.locator(SignInLocators.EMAIL_INPUT).fill(email)
        page.locator(SignInLocators.PASSWORD_INPUT).fill(password)

        expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_enabled()

        page.locator(SignInLocators.LOGIN_BUTTON).click()

        expect(page.locator(SignInLocators.GENERAL_ERROR)).to_contain_text(expected_error)
        expect(page).to_have_url(f"{BASE_URL}/login")

        @allure.title("Email validation error is shown after clearing email field")
        def test_empty_email_error_after_clearing_field(self, page):
            self.open_login_page(page)

            page.locator(SignInLocators.EMAIL_INPUT).fill("test@email.com")
            page.locator(SignInLocators.EMAIL_INPUT).fill("")
            page.locator(SignInLocators.PASSWORD_INPUT).click()

            expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()
            expect(page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text("Email address is required")

            @allure.title("Password validation error is shown after clearing password field")
            def test_empty_password_error_after_clearing_field(self, page):
                self.open_login_page(page)

                page.locator(SignInLocators.EMAIL_INPUT).fill("test@email.com")
                page.locator(SignInLocators.PASSWORD_INPUT).fill("Test@1234!")
                page.locator(SignInLocators.PASSWORD_INPUT).fill("")
                page.locator(SignInLocators.EMAIL_INPUT).click()

                expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()
                expect(page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text("Password is required")

    @allure.title("User is blocked for 15 minutes after 5 failed login attempts")
    @pytest.mark.skip(reason="Account lock after 5 failed attempts is not implemented yet")
    def test_user_blocked_after_5_failed_login_attempts(self, page):
        self.open_login_page(page)

        email = "xonib78658@inreur.com"
        wrong_password = "WrongPass123!"
        expected_error = "Incorrect email or password"
        expected_block_message = "Your account is temporarily locked"

        for attempt in range(5):
            page.locator(SignInLocators.EMAIL_INPUT).fill(email)
            page.locator(SignInLocators.PASSWORD_INPUT).fill(wrong_password)

            expect(page.locator(SignInLocators.LOGIN_BUTTON)).to_be_enabled()

            page.locator(SignInLocators.LOGIN_BUTTON).click()

            if attempt < 4:
                expect(page.locator(SignInLocators.GENERAL_ERROR)).to_contain_text(expected_error)

        expect(page.locator(SignInLocators.GENERAL_ERROR)).to_contain_text(expected_block_message)
        expect(page).to_have_url(f"{BASE_URL}/login")
