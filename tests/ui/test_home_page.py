import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.home_page import HomePage
from tests.ui.data.home_page_data import NAV_ITEMS

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@allure.parent_suite("UI Tests")
@allure.suite("Home Page")
@allure.sub_suite("Navigation")
class _HomePageBase:
    """Shared Allure hierarchy for home page test classes."""


@allure.story("Page title")
class TestHomePageTitle(_HomePageBase):

    @allure.title("Page title is 'PRetty'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_title(self, page):
        with allure.step("Open home page"):
            home = HomePage(page)
            home.open()
        with allure.step("Verify page title is 'PRetty'"):
            home.expect_title("PRetty")


@allure.story("Navigation links")
class TestHomePageNavigation(_HomePageBase):
    test_data_map = {"nav_item": NAV_ITEMS}

    @allure.title("Nav item is visible: {nav_item}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_links_present(self, page, nav_item):
        with allure.step("Open home page"):
            home = HomePage(page)
            home.open()
        with allure.step(f"Verify '{nav_item['label']}' nav button is visible"):
            expect(home.get_nav_button(nav_item["label"])).to_be_visible()
