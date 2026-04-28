import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.home_page import HomePage
from tests.ui.data.home_page_data import NAV_ITEMS


@pytest.mark.ui
@allure.suite("Home Page")
class TestHomePage:

    @allure.title("Page title is 'PRetty'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_title(self, page):
        with allure.step("Open home page"):
            home = HomePage(page)
            home.open()
        with allure.step("Verify page title is 'PRetty'"):
            home.expect_title("PRetty")

    @pytest.mark.parametrize("nav_item", NAV_ITEMS)
    @allure.title("Nav item is visible: {nav_item}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_links_present(self, page, nav_item):
        with allure.step("Open home page"):
            home = HomePage(page)
            home.open()
        with allure.step(f"Verify '{nav_item}' nav button is visible"):
            expect(home.get_nav_button(nav_item)).to_be_visible()