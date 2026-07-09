import allure
import pytest
from allure_commons.types import Severity as severity_level

from framework.ui.pages.atm_page import AtmPage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.epic("UI")
@allure.feature("Search and filter ATM's and branches")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.11.1 Search and Filter ATM's and Branches")
class _AtmBase:
    pass


@allure.story("Search and Filter ATM's and Branches")
class TestAtmAndBranches(_AtmBase):

    @allure.title("View all ATM's and branches")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-174")
    def test_view_all_atms_and_branches(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Verify the ATM landing layot view renders all elements"):
            atm_page.expect_atm_page_is_opened()
            atm_page.expect_map_is_visible()
            atm_page.expect_list_is_visible()

    @allure.title("User is on ATMS and branches page with map and list visible")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-175")
    def test_user_is_on_atms_and_branches_page_with_map_and_list_visible(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Click on a location card in the sidebar list"):
            clicked_name, _ = atm_page.click_location_card(0)
            atm_page.expect_popup_shows_same_location(clicked_name)

        with allure.step("Click on a map pin"):
            clicked_pin = atm_page.click_location_pin(1)
            parts = clicked_pin.split(" ")
            atm_page.expect_popup_shows_same_location(f"{parts[-2]} no. {parts[-1]}")

    @allure.title("Filter atms and branches by service type")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-176")
    def test_filter_atms_and_branches_by_service_type(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Click on the ATM's service type filter option"):
            atm_page.click_service_type_filter("ATMs")
            atm_page.expect_only_atms_displayed()

        with allure.step("Apply a specific city location filter"):
            atm_page.click_city_filter("Gdansk")
            atm_page.expect_only_atms_in_city_displayed("Gdansk")

    @allure.title("Verify search bar functionality")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-177")
    def test_verify_search_bar_functionality(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Enter a specific valid city in the search bar"):
            atm_page.enter_city_name("Warszawa")
            atm_page.expect_matching_locations_in_list_and_on_map("Warszawa")

        with allure.step("Clear search history inpits and query a wrong city"):
            atm_page.enter_city_name("sadaqwhfkygq")
            atm_page.expect_wrong_city()

    @allure.title("Map pin interaction")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-178")
    def test_map_pin_interaction(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Interact with clustered overlapping layot pins"):
            atm_page.click_sub_pin()
            clicked_sub_pin = atm_page.click_sub_pin()
            parts = clicked_sub_pin.split(" ")
            atm_page.expect_popup_shows_same_location(f"{parts[-2]} no. {parts[-1]}")

    @allure.title("Verify branch/ATM location details in list and map")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-179")
    def test_verify_branch_and_atm_location_details_in_list_and_map(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Select a valid specific branch item row from the sidebar list"):
            clicked_name, _ = atm_page.click_location_card(0)
            hours = atm_page.get_card_hours(0)
            atm_page.expect_popup_shows_same_location(clicked_name)
            atm_page.expect_popup_shows_same_hours(hours)

        with allure.step("Correlate matching structural metadata by selecting items from the map grid"):
            clicked_pin = atm_page.click_location_pin(1)
            parts = clicked_pin.split(" ")
            atm_page.expect_popup_shows_same_location(f"{parts[-2]} no. {parts[-1]}")
            atm_page.expect_popup_shows_same_hours_visible()

    @allure.story("Verify paginations of locations list")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-180")
    @pytest.mark.skip(
        reason="There are fewer locations in the test, so pagination controls (< >) do not render on the UI."
    )
    def test_verify_paginations_of_locations_list(self, page):
        pass

    @allure.title("Verify clearing selected city filter")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-363")
    def test_verify_clearing_selected_city_filter(self, page):
        atm_page = AtmPage(page)

        with allure.step("Navigate to the ATMs and branches section"):
            atm_page.click_atm_button()

        with allure.step("Query dynamic search fields to isolate entries"):
            atm_page.enter_city_name("Warszawa")
            warszawa_count = atm_page.get_card_count()

        with allure.step("Clear query values and verify container grid reset automatically to full capacity"):
            atm_page.clear_city_name()
            all_count = atm_page.get_card_count()
            assert all_count > warszawa_count
