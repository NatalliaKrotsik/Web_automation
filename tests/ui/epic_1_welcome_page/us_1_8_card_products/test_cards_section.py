import allure
import pytest

from framework.ui.pages.home_page import HomePage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Card Products")
@allure.sub_suite("US-1.8 Show Card Products on the Welcome Page")
class TestCardsSection:

    @allure.title("LP-221 — Click 'Cards' on navigation panel")
    @pytest.mark.qase("LP-221")
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_cards_section_visible_on_click(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Verify 'Cards' section is visible"):
            home.expect_cards_are_visible()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-221 — Reload the page and manually scroll down to the 'Cards' section")
    @pytest.mark.qase("LP-221")
    @pytest.mark.regression
    def test_cards_section_visible_on_scroll(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Scroll to cards section"):
            home.scroll_to_cards()
        with allure.step("Verify 'Cards' section is visible"):
            home.expect_cards_are_visible()
