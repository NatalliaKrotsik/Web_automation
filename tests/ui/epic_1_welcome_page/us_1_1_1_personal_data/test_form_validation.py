import allure
import pytest

from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestFormValidation:

    @allure.title("TC-04 — Invalid first name shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_first_name_shows_error(self, page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        invalid = personal_info_data["invalid"]["first_name"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step(f"Fill First Name with invalid value: {invalid['value']}"):
            personal_info.fill_first_name(invalid["value"])
            personal_info.last_name_input().click()

        with allure.step("Assert error message is visible with correct text"):
            personal_info.expect_field_error_visible("firstName", invalid["expected_error"])

    @allure.title("TC-04 — Invalid middle name shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_middle_name_shows_error(self, page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        invalid = personal_info_data["invalid"]["middle_name"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step(f"Fill Middle Name with invalid value: {invalid['value']}"):
            personal_info.fill_middle_name(invalid["value"])
            personal_info.last_name_input().click()

        with allure.step("Assert error message is visible with correct text"):
            personal_info.expect_field_error_visible("middleName", invalid["expected_error"])

    @allure.title("TC-04 — Invalid last name shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_last_name_shows_error(self, page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        invalid = personal_info_data["invalid"]["last_name"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step(f"Fill Last Name with invalid value: {invalid['value']}"):
            personal_info.fill_last_name(invalid["value"])
            personal_info.first_name_input().click()

        with allure.step("Assert error message is visible with correct text"):
            personal_info.expect_field_error_visible("lastName", invalid["expected_error"])

    @allure.title("TC-04 — Invalid passport ID shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_passport_id_shows_error(self, page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        invalid = personal_info_data["invalid"]["passport_id"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step(f"Fill Passport ID with invalid value: {invalid['value']}"):
            personal_info.fill_passport_id(invalid["value"])
            personal_info.first_name_input().click()

        with allure.step("Assert error message is visible with correct text"):
            personal_info.expect_field_error_visible("passportId", invalid["expected_error"])

    @allure.title("TC-66 — Invalid birth date shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_birth_date_shows_error(self, page, personal_info_data) -> None:
        personal_info = PersonalInfoPage(page)
        invalid = personal_info_data["invalid"]["birth_date"]

        with allure.step("Open sign up page"):
            personal_info.open()

        with allure.step(f"Fill Birth Date with invalid value: {invalid['value']}"):
            personal_info.fill_birth_date(invalid["value"])
            personal_info.first_name_input().click()

        with allure.step("Assert error message is visible with correct text"):
            personal_info.expect_field_error_visible("birthDate", invalid["expected_error"])