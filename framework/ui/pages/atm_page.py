from playwright.sync_api import expect

from framework.ui.core.base_page import BasePage


class AtmPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://dev.pretty-py.andersenlab.dev/")
        self.page = page
        self._atms_button = page.get_by_role("button", name="ATMs")
        self._location_list = page.locator("ul.divide-border-main")
        self._location_card = page.locator("li.flex.max-w-md.cursor-pointer")
        self._map_popup_title = page.locator(".gm-style-iw-d h3")
        self._map_popup_hours = page.locator(".gm-style-iw-d p.text-sm")
        self._map_pin = page.locator('gmp-advanced-marker[slot*="visible"]')
        self._filter_service_type_section = page.locator("h2", has_text="Service type").locator(
            "xpath=following-sibling::div[1]"
        )
        self._filter_city_section = page.locator("h2", has_text="Cities where we are").locator(
            "xpath=following-sibling::div[1]"
        )
        self._filter_all = self._filter_service_type_section.get_by_role("button", name="ALL", exact=True)
        self._filter_atms = self._filter_service_type_section.get_by_role("button", name="ATMs", exact=True)
        self._filter_branches = self._filter_service_type_section.get_by_role("button", name="Branches", exact=True)
        self._city_search_bar = page.get_by_placeholder("Search by city or address…")
        self._wrong_city = page.get_by_text("No location found")

    def open(self):
        self.page.goto("https://dev.pretty-py.andersenlab.dev/")

    def click_atm_button(self):
        self.open()
        self._atms_button.click()

    def expect_atm_page_is_opened(self):
        expect(self.page).to_have_url("https://dev.pretty-py.andersenlab.dev/locations")

    def expect_map_is_visible(self):
        expect(self.page.locator(".gm-style")).to_be_visible()

    def expect_list_is_visible(self):
        expect(self._location_list).to_be_visible()

    def user_is_on_atms_an_branches_page(self):
        self.click_atm_button()
        self.expect_atm_page_is_opened()
        self.expect_map_is_visible()
        self.expect_list_is_visible()

    def click_location_card(self, index=0):
        card = self._location_card.nth(index)
        name = card.locator("h3").text_content()
        city = card.locator("p").nth(0).text_content().split(", ")[-1]
        card.click()
        return name, city

    def click_location_pin(self, index=0):
        pins = self._map_pin
        pin = pins.nth(index)
        name = pin.get_attribute("aria-label")
        pin.click()
        return name

    def expect_popup_shows_same_location(self, expected_name):
        expect(self._map_popup_title).to_have_text(expected_name)

    def click_service_type_filter(self, filter_name: str):
        if filter_name == "ALL":
            self._filter_all.click()
        elif filter_name == "ATMs":
            self._filter_atms.click()
        elif filter_name == "Branches":
            self._filter_branches.click()

    def click_city_filter(self, city: str):
        self._filter_city_section.get_by_role("button", name=city, exact=True).click()

    def expect_only_atms_displayed(self):
        cards = self._location_card.all_text_contents()
        for card_text in cards:
            assert "ATM" in card_text
            assert "Branch" not in card_text

    def expect_only_atms_in_city_displayed(self, city):
        cards = self._location_card.all_text_contents()

        for card_text in cards:
            assert "ATM" in card_text
            assert "Branch" not in card_text
            assert city in card_text

    def get_visible_pin_count(self):
        return self.page.locator('gmp-advanced-marker[slot*="visible"]').count()

    def get_card_count(self):
        return self._location_card.count()

    def expect_map_and_list_counts_match(self):
        pin_match = self.get_visible_pin_count()
        card_match = self.get_card_count()

        assert pin_match == card_match

    def enter_city_name(self, city):
        self._city_search_bar.fill(city)

    def clear_city_name(self):
        self._city_search_bar.clear()

    def expect_matching_locations_in_list_and_on_map(self, city):
        cards = self._location_card.all_text_contents()

        for card_text in cards:
            assert city in card_text

    def expect_wrong_city(self):
        expect(self._wrong_city).to_be_visible()

    def click_sub_pin(self, parent_index=0, sub_index=0):
        self.click_location_pin(index=parent_index)
        self.page.wait_for_timeout(1000)
        sub_pins = self._map_pin
        chosen_pin = sub_pins.nth(sub_index)
        sub_pin_name = chosen_pin.get_attribute("aria-label")
        chosen_pin.click()
        return sub_pin_name

    def get_card_hours(self, index=0):
        card = self._location_card.nth(index)
        return card.locator("p").nth(1).text_content()

    def expect_popup_shows_same_hours(self, expected_hours):
        expect(self._map_popup_hours).to_have_text(expected_hours)

    def expect_popup_shows_same_hours_visible(self):
        expect(self._map_popup_hours).to_be_visible()
