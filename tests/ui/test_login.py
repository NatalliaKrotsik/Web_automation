import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.login_page import LoginPage
from tests.ui.data.login_data import (
    BOTH_FIELDS_EMPTY,
    EMPTY_EMAIL,
    EMPTY_PASSWORD,
    INVALID_EMAIL_FORMAT,
    INVALID_PASSWORD,
    get_valid_user,
)


@pytest.mark.ui
@pytest.mark.smoke
@allure.suite("Authentication")
class TestLogin:

    @pytest.mark.qase("PRETTY-229")
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_valid_credentials(self, page):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Fill in valid email and password"):
            user = get_valid_user()
            login.fill_email(user["email"])
            login.fill_password(user["password"])
        with allure.step("Click Log in button"):
            login.click_login()
        with allure.step("Verify redirect to home"):
            login.expect_redirected_to_home()

    @pytest.mark.qase("PRETTY-230")
    @allure.title("Login fails with invalid password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("credentials", [INVALID_PASSWORD])
    def test_login_with_invalid_password(self, page, credentials):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Submit invalid password"):
            login.login(credentials["email"], credentials["password"])
        with allure.step("Verify error message is shown"):
            login.expect_error_message("Incorrect email or password")

    @pytest.mark.qase("PRETTY-227")
    @allure.title("Login button disabled with invalid input: {credentials}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("credentials", [
        INVALID_EMAIL_FORMAT,
        EMPTY_EMAIL,
        EMPTY_PASSWORD,
        BOTH_FIELDS_EMPTY,
    ])
    def test_login_blocked_with_invalid_input(self, page, credentials):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step("Fill form with invalid input"):
            login.fill_login_form(credentials["email"], credentials["password"])
        with allure.step("Verify login button is disabled"):
            expect(login._login_button).to_be_disabled()