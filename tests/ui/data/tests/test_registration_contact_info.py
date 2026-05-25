import allure
import pytest

from framework.ui.pages.registration_contact_info import RegistrationPage
from tests.ui.data.registration_contact_info_data import (
    INVALID_EMAILS,
    INVALID_PHONES,
    VALID_EMAILS,
    VALID_PHONES,
)


@pytest.mark.ui
@allure.suite("Registration")
class TestRegistrationContactInfo:

    @allure.title("Registration continues with valid email")
    @pytest.mark.parametrize("email", VALID_EMAILS)
    def test_valid_email_on_contact_info_step(self, page, email):
        registration = RegistrationPage(page)

        with allure.step("Navigate to Contact Info step"):
            registration.go_to_contact_info_step()

        with allure.step("Fill Email field with valid data"):
            registration.fill_email(email)

        with allure.step("Fill Phone field with valid data"):
            registration.fill_phone("+359 881234567")

        with allure.step("Click Continue button"):
            registration.click_continue()

        with allure.step("Verify user is redirected to the next registration step"):
            registration.expect_next_registration_step()

    @allure.title("Registration shows error message with invalid email")
    @pytest.mark.parametrize("data", INVALID_EMAILS)
    def test_invalid_email_on_contact_info_step(self, page, data):
        registration = RegistrationPage(page)

        with allure.step("Navigate to Contact Info step"):
            registration.go_to_contact_info_step()

        with allure.step("Fill Email field with invalid data"):
            registration.fill_email(data["email"])

        with allure.step("Fill Phone field with valid data"):
            registration.fill_phone("+359 881234567")

        with allure.step("Verify email error message is shown"):
            registration.expect_email_error_message(data["expected_error"])

    @allure.title("Registration continues with valid phone")
    @pytest.mark.parametrize("phone", VALID_PHONES)
    def test_valid_phone_on_contact_info_step(self, page, phone):
        registration = RegistrationPage(page)

        with allure.step("Navigate to Contact Info step"):
            registration.go_to_contact_info_step()

        with allure.step("Fill Email field with valid data"):
            registration.fill_email("alina.petrova@gmail.com")

        with allure.step("Fill Phone field with valid data"):
            registration.fill_phone(phone)

        with allure.step("Click Continue button"):
            registration.click_continue()

        with allure.step("Verify user is redirected to the next registration step"):
            registration.expect_next_registration_step()

    @allure.title("Registration shows error message with invalid phone")
    @pytest.mark.parametrize("data", INVALID_PHONES)
    def test_invalid_phone_on_contact_info_step(self, page, data):
        registration = RegistrationPage(page)

        with allure.step("Navigate to Contact Info step"):
            registration.go_to_contact_info_step()

        with allure.step("Fill Email field with valid data"):
            registration.fill_email("alina.petrova@gmail.com")

        with allure.step("Fill Phone field with invalid data"):
            registration.fill_phone(data["phone"])

        with allure.step("Verify phone error message is shown"):
            registration.expect_phone_error_message(data["expected_error"])
