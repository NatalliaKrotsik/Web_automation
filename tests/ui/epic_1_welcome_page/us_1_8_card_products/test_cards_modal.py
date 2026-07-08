import allure
import pytest

from framework.ui.pages.home_page import HomePage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Card Products")
@allure.sub_suite("US-1.8 Show Card Products on the Welcome Page")
class TestCardsModal:
    @allure.title("LP-222 — Click 'Open a card' locate 'X' and click it to close modal")
    @pytest.mark.qase("LP-222")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_closes_on_x_button(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Click on 'open a card' button"):
            home.click_open_a_card()
        with allure.step("Check if X button is visible"):
            home.expect_x_button_is_visible()
        with allure.step("Click on X button"):
            home.click_x_button()
        with allure.step("Check if modal is closed"):
            home.expect_modal_is_closed()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-222 — Click 'Open a card' locate 'Cancel' and click it to close modal")
    @pytest.mark.qase("LP-222")
    @pytest.mark.regression
    def test_modal_closes_on_cancel_button(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Click on 'open a card' button"):
            home.click_open_a_card()
        with allure.step("Check if Cancel button is visible"):
            home.expect_cancel_button_is_visible()
        with allure.step("Click on Cancel button"):
            home.click_close_button()
        with allure.step("Check if modal is closed"):
            home.expect_modal_is_closed()

    @allure.title("LP-342 — Verify card application modal displays correct content")
    @pytest.mark.qase("LP-342")
    @allure.severity(allure.severity_level.MINOR)
    def test_modal_content_is_correct(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Click on 'open a card' button"):
            home.click_open_a_card()
        with allure.step("Check if Modal shows title 'apply for {card name}'"):
            home.expect_modal_is_open()
        with allure.step("Check if modal message says: 'Select how you would like to proceed' "):
            home.expect_modal_message_is_visible()
        with allure.step("Check Log in, Sign up, Close options are visible"):
            home.expect_modal_options_visible()
        with allure.step("Check if Cancel button is visible"):
            home.expect_cancel_button_is_visible()

    @allure.title("LP-349 — Verify login redirect from card application modal")
    @pytest.mark.qase("LP-349")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_redirects_to_login(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Click on 'open a card' button"):
            home.click_open_a_card()
        with allure.step("Click on 'existing profile'"):
            home.click_existing_profile()
        with allure.step("Verify redirection to Login page"):
            home.expect_redirect_to_login()

    @allure.title("LP-349 — Verify sign up redirect from card application modal")
    @pytest.mark.qase("LP-349")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_modal_redirects_to_signup(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Click on 'open a card' button"):
            home.click_open_a_card()
        with allure.step("Click on 'New Profile'"):
            home.click_new_profile()
        with allure.step("Verify redirection to Sign up page"):
            home.expect_redirect_to_signup()
