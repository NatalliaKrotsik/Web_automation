import allure
import pytest

from playwright.sync_api import Page, expect

from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestHappyPath:

    @allure.title("TC-01 — Fill valid data and continue to Contact Details")
    @pytest.mark.regression
    def test_valid_data_navigates_to_contact_details(self, page: Page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        valid = personal_info_data["valid"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step("Fill all required fields with valid data"):
            personal_info.fill_required_fields(
                first_name=valid["first_name"],
                last_name=valid["last_name"],
                passport_id=valid["passport_id"],
                birth_date=valid["birth_date"],
            )

        with allure.step("Assert Continue button is enabled"):
            personal_info.expect_continue_button_enabled()

        with allure.step("Click Continue"):
            personal_info.click_continue()

        with allure.step("Assert Contact Details heading is visible"):
            expect(page.get_by_role("heading", name="Contact Details")).to_be_visible()