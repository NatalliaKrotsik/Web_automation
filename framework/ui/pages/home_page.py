from playwright.sync_api import Page, expect

from framework.env_manager import EnvManager
from framework.ui.core.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page, EnvManager.get_config().base_url)

    def get_nav_button(self, name: str):
        return self.page.get_by_role("button", name=name, exact=True)

    def expect_title(self, title: str) -> None:
        expect(self.page).to_have_title(title)
