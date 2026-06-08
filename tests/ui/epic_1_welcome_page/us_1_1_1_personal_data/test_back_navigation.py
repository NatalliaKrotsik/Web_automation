import allure
import pytest

from playwright.sync_api import Page

from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestBackNavigation:

    @allure.title("TC-76 — Fields pre-filled when navigating back from Contact Details")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_fields_pre_filled_after_back_navigation(self, page: Page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        valid = personal_info_data["valid"]

        with allure.step("Open sign up page and fill all required fields"):
            personal_info.open()
            personal_info.fill_required_fields(
                first_name=valid["first_name"],
                last_name=valid["last_name"],
                passport_id=valid["passport_id"],
                birth_date=valid["birth_date"],
            )

        with allure.step("Click Continue to navigate to Contact Details"):
            personal_info.click_continue()

        with allure.step("Click Back to personal info"):
            personal_info.click_back()

        with allure.step("Assert all fields are still pre-filled with original values"):
            personal_info.expect_field_value("firstName", valid["first_name"])
            personal_info.expect_field_value("lastName", valid["last_name"])
            personal_info.expect_field_value("passportId", valid["passport_id"])
            personal_info.expect_field_value("birthDate", valid["birth_date"])

    @allure.title("TC-77 — Re-validation triggers after navigating back and editing invalid value")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_revalidation_after_back_navigation(self, page: Page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        valid = personal_info_data["valid"]
        invalid = personal_info_data["invalid"]["last_name"]

        with allure.step("Open sign up page and fill all required fields"):
            personal_info.open()
            personal_info.fill_required_fields(
                first_name=valid["first_name"],
                last_name=valid["last_name"],
                passport_id=valid["passport_id"],
                birth_date=valid["birth_date"],
            )

        with allure.step("Click Continue to navigate to Contact Details"):
            personal_info.click_continue()

        with allure.step("Click Back to personal info"):
            personal_info.click_back()

        with allure.step(f"Edit Last Name to invalid value: {invalid['value']}"):
            personal_info.fill_last_name(invalid["value"])
            personal_info.first_name_input().click()

        with allure.step("Assert error message is visible"):
            personal_info.expect_field_error_visible("lastName", invalid["expected_error"])