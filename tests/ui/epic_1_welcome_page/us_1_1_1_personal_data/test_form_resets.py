import allure
import pytest

from playwright.sync_api import Page

from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure hierarchy for personal info test classes."""


@allure.story("Form resets")
class TestFormResets(_PersonalInfoBase):

    @allure.title("TC-78 — Fields are empty after page reload")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_fields_empty_after_reload(self, page: Page, personal_info_data) -> None:
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

        with allure.step("Reload the page"):
            personal_info.refresh_page()

        with allure.step("Assert all fields are empty after reload"):
            personal_info.expect_field_value("firstName", "")
            personal_info.expect_field_value("lastName", "")
            personal_info.expect_field_value("passportId", "")
            personal_info.expect_field_value("birthDate", "")

    @allure.title("TC-79 — Fields are empty after closing and reopening tab")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_fields_empty_after_tab_close(self, context, personal_info_data) -> None:
        valid = personal_info_data["valid"]

        with allure.step("Open sign up page and fill all required fields"):
            page1 = context.new_page()
            personal_info = PersonalInfoPage(page1)
            personal_info.open()
            personal_info.fill_required_fields(
                first_name=valid["first_name"],
                last_name=valid["last_name"],
                passport_id=valid["passport_id"],
                birth_date=valid["birth_date"],
            )

        with allure.step("Close the tab"):
            page1.close()

        with allure.step("Open a new tab and navigate to sign up"):
            page2 = context.new_page()
            personal_info2 = PersonalInfoPage(page2)
            personal_info2.open()

        with allure.step("Assert all fields are empty"):
            personal_info2.expect_field_value("firstName", "")
            personal_info2.expect_field_value("lastName", "")
            personal_info2.expect_field_value("passportId", "")
            personal_info2.expect_field_value("birthDate", "")