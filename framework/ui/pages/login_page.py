"""Page Object for the Login page."""
from playwright.sync_api import Page, expect

from framework.env_manager import EnvManager
from framework.ui.core.base_page import BasePage

class LoginPage(BasePage):
    """Represents the Login page of PRetty Online Banking."""

    def __init__(self, page: Page):
        super().__init__(page, EnvManager.get_config().base_url + "/login")
        self._email_input = page.get_by_placeholder("email@email.com")
        self._password_input = page.get_by_placeholder("••••••")
        self._login_button = page.get_by_role("button", name="Log in", exact=True).last
        self._error_message = page.locator(".bg-labels-red")

    def fill_email(self, email: str) -> None:
        self._email_input.fill(email)

    def fill_password(self, password: str) -> None:
        self._password_input.fill(password)

    def fill_login_form(self, email: str, password: str) -> None:
        self.fill_email(email)
        self.fill_password(password)

    def click_login(self) -> None:
        self._login_button.click()

    def login(self, email: str, password: str) -> None:
        self.fill_login_form(email, password)
        self.click_login()

    def expect_error_message(self, message: str) -> None:
        expect(self._error_message).to_be_visible()
        expect(self._error_message).to_contain_text(message)

    def expect_redirected_to_home(self) -> None:
        self.wait_for_the_url("**/home**")