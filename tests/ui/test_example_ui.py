import allure
import pytest

from framework.ui.pages.example_page import ExamplePage

@pytest.mark.ui
class TestExampleUI:

    @allure.suite("US-1.1 General info about the bank")
    @allure.severity(allure.severity_level.NORMAL)
    def test_check_click_home_logo(self, page):
        main = ExamplePage(page)
        main.open()
        main.click_logo()

    def test_clicking_login_btn(self, page):
        main = ExamplePage(page)
        main.open()
        main.click_log_in()

    def test_checking_singup_btn(self, page):
        main = ExamplePage(page)
        main.open()
        main.click_log_in()
        main.click_sign_up()