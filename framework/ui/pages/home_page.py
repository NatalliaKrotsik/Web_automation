from playwright.sync_api import Page, expect

from framework.env_manager import EnvManager
from framework.ui.core.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page, EnvManager.get_config().base_url)
        self._card_heading = page.get_by_role("heading", name="Карты" or "Cards", level=2)
        self._cards_by_button = page.get_by_role("button", name="Open a Card")
        self._cancel_button = page.get_by_role("button", name="Cancel")
        self._x_button = page.get_by_test_id("modal-close-btn")
        self._modal_heading = page.get_by_role("heading", name="Apply for", level=1)
        self._modal_message = page.get_by_text("Select how you would like to proceed")
        self._modal_login_option = page.get_by_role("heading", name="Existing profile", level=2)
        self._modal_sign_up_option = page.get_by_role("heading", name="New profile", level=2)

    def get_nav_button(self, name: str):
        return self.page.get_by_role("button", name=name)

    def scroll_to_cards(self):
        self._card_heading.scroll_into_view_if_needed()

    # Expects

    def expect_title(self, title: str) -> None:
        expect(self.page).to_have_title(title)

    def expect_cards_are_visible(self):
        expect(self._card_heading).to_be_visible()
        expect(self._cards_by_button.first).to_be_visible()

    def expect_modal_is_open(self):
        expect(self._modal_heading).to_be_visible()

    def expect_modal_is_closed(self):
        expect(self._modal_heading).not_to_be_visible()

    def expect_x_button_is_visible(self):
        expect(self._x_button).to_be_visible()

    def expect_cancel_button_is_visible(self):
        expect(self._cancel_button).to_be_visible()

    def expect_modal_message_is_visible(self):
        expect(self._modal_message).to_be_visible()

    def expect_modal_options_visible(self):
        expect(self._modal_login_option).to_be_visible()
        expect(self._modal_sign_up_option).to_be_visible()

    def expect_redirect_to_login(self):
        expect(self.page).to_have_url("**/login")

    def expect_redirect_to_signup(self):
        expect(self.page).to_have_url("**/sign-up")

    # Actions

    def click_x_button(self):
        self._x_button.click()

    def click_close_button(self):
        self._cancel_button.click()

    def click_open_a_card(self):
        self._cards_by_button.first.click()

    def click_existing_profile(self):
        self._modal_login_option.click()

    def click_new_profile(self):
        self._modal_sign_up_option.click()
