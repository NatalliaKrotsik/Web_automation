import pytest
from playwright.sync_api import Page

from framework.ui.pages.home_page import HomePage
from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage

class TestPageOpen:

    def test_sign_up_opens_personal_info_form(self, page: Page) -> None:
        home = HomePage(page)
        personal_info = PersonalInfoPage(page)

        home.open()
        home.get_nav_button("Sign up").click()

        personal_info.expect_page_heading_visible()
        personal_info.expect_all_fields_visible()
        personal_info.expect_continue_button_disabled()