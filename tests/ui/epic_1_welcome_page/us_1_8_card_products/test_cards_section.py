import allure
import pytest

from framework.ui.pages.home_page import HomePage

pytestmark = [pytest.mark.ui, pytest.mark.regression]



@allure.parent_suite("UI Tests")
@allure.suite("Card Products")
@allure.sub_suite("US-1.8 Show Card Products on the Welcome Page")
class _CardSectionBase:
    """Shared Allure hierarchy for cards section test classes."""


@allure.story("Cards section visibility")
class TestCardsSection(_CardSectionBase):

    @allure.title("LP-221 — Cards section visible after clicking 'Cards' navigation button")
    @pytest.mark.qase("LP-221")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cards_section_visible_on_click(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Verify 'Cards' section is visible"):
            home.expect_cards_are_visible()

    @allure.title("LP-362 — Cards section visible after scrolling to it")
    @pytest.mark.qase("LP-362")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cards_section_visible_on_scroll(self, page):
        home = HomePage(page)
        with allure.step("Open home page"):
            home.open()
        with allure.step("Scroll to cards section"):
            home.scroll_to_cards()
        with allure.step("Verify 'Cards' section is visible"):
            home.expect_cards_are_visible()
