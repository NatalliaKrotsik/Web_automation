from playwright.sync_api import expect

from framework.ui.core.base_page import BasePage
from tests.api.epic_1_welcome_page.data.address_data import valid_address


class RegistrationPage(BasePage):

    def __init__(self, page):
        super().__init__(page, "https://dev.example.com/sign-up")
        self.page = page

        # Step 1: Personal information
        self._first_name_input = page.locator("#firstName")
        self._middle_name_input = page.locator("#middleName")
        self._last_name_input = page.locator("#lastName")
        self._passport_id_input = page.locator("#passportId")
        self._birth_date_input = page.get_by_placeholder("DD/MM/YYYY")

        # Common button
        self._continue_button = page.get_by_role("button", name="Continue")

        # Step 2: Contact details
        self._email_input = page.get_by_label("Email")
        self._phone_input = page.get_by_label("Phone number")

        # Step 3: Address Information
        self._street_input = page.locator("#registrationAddress\\.street")
        self._house_number_input = page.locator("#registrationAddress\\.houseNumber")
        self._apartment_input = page.locator("#registrationAddress\\.apartment")
        self._postal_code_input = page.locator("#registrationAddress\\.postalCode")
        self._city_input = page.locator("#registrationAddress\\.city")
        # self._country_input = page.locator("#registrationAddress\\.country")

        self._billing_same_checkbox = page.get_by_text("The Billing address is the same as the registration address.")

        self._billing_street_input = page.locator("#billingAddress\\.street")
        self._billing_house_number_input = page.locator("#billingAddress\\.houseNumber")
        self._billing_apartment_input = page.locator("#billingAddress\\.apartment")
        self._billing_postal_code_input = page.locator("#billingAddress\\.postalCode")
        self._billing_city_input = page.locator("#billingAddress\\.city")
        # self._billing_country_input = page.locator("#billingAddress\\.country")

        # Step 4: Email Verification
        self._otp_inputs = page.locator("input[autocomplete='one-time-code']")
        self._verify_button = page.get_by_role("button", name="Verify")
        self._resend_code = page.get_by_role("button", name="Resend Code")
        self._resend_code_countdown = page.get_by_text("Resend code in")

    def open(self):
        self.page.goto("https://dev.example.com/sign-up")

    def fill_personal_information_step_with_valid_data(self):
        self._first_name_input.fill("John")
        self._middle_name_input.fill("Michael")
        self._last_name_input.fill("Doe")
        self._passport_id_input.fill("123456789")
        self._birth_date_input.fill("02/01/1990")
        # self.page.get_by_role("button", name="2", exact=True).click()

    def click_continue(self):
        self._continue_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        self._continue_button.click(force=True)

    def go_to_contact_info_step(self):
        self.open()
        self.fill_personal_information_step_with_valid_data()
        self.click_continue()
        self.expect_contact_info_step_is_opened()

    def fill_email(self, email):
        self._email_input.fill(email)

    def fill_phone(self, phone):
        self._phone_input.fill(phone)

    def expect_contact_info_step_is_opened(self):
        expect(self._email_input).to_be_visible()
        expect(self._phone_input).to_be_visible()

    def expect_next_registration_step(self):
        expect(self.page.get_by_text("Email Verification")).to_be_visible()

    def expect_email_error_message(self, expected_error):
        expect(self.page.get_by_text(expected_error)).to_be_visible()

    def expect_phone_error_message(self, expected_error):
        expect(self.page.get_by_text(expected_error)).to_be_visible()

    def fill_address_step_with_valid_data(self, registration=valid_address):
        reg_address = registration["registrationAddress"]
        self._street_input.fill(reg_address["street"])
        self._house_number_input.fill(reg_address["houseNumber"])
        self._apartment_input.fill(reg_address["apartment"])
        self._postal_code_input.fill(reg_address["postalCode"])
        self._city_input.fill(reg_address["city"])
        # self._country_input.fill(reg_address["country"])

        if registration["billingSameAsRegistration"]:
            self._billing_same_checkbox.click()
        else:
            billing = registration["billingAddress"]
            self._billing_street_input.fill(billing["street"])
            self._billing_house_number_input.fill(billing["houseNumber"])
            self._billing_apartment_input.fill(billing["apartment"])
            self._billing_postal_code_input.fill(billing["postalCode"])
            self._billing_city_input.fill(billing["city"])
            # self._billing_country_input.fill(billing["country"])

    def expect_address_info_is_opened(self):
        expect(self._street_input).to_be_visible()
        expect(self._house_number_input).to_be_visible()
        expect(self._apartment_input).to_be_visible()
        expect(self._postal_code_input).to_be_visible()
        expect(self._city_input).to_be_visible()
        # expect(self._country_input).to_be_visible()
        expect(self._billing_street_input).to_be_visible()
        expect(self._billing_house_number_input).to_be_visible()
        expect(self._billing_apartment_input).to_be_visible()
        expect(self._billing_postal_code_input).to_be_visible()
        expect(self._billing_city_input).to_be_visible()
        # expect(self._billing_country_input).to_be_visible()

    def fill_otp(self, otp):
        for i, digit in enumerate(otp):
            self._otp_inputs.nth(i).fill(digit)

    def click_verify(self):
        self._verify_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        self._verify_button.click(force=True)

    def expect_click_verify_to_be_disabled(self):
        expect(self._verify_button).to_be_disabled()

    def expect_otp_error_message(self, expected_error):
        self.page.wait_for_timeout(1000)
        expect(self.page.get_by_text(expected_error)).to_be_visible()

    def click_resend_code(self):
        self._resend_code.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        self._resend_code.click(force=True)

    def expect_click_resend_code_is_not_clickable(self):
        expect(self._resend_code_countdown).to_be_visible()

    def expect_otp_is_locked(self):
        expect(self.page.get_by_text("Too many failed attempts")).to_be_visible()
        expect(self._resend_code_countdown).to_be_visible()
        expect(self._verify_button).to_be_disabled()

    def otp_is_locked(self) -> bool:
        return self.page.get_by_text("Too many failed attempts").is_visible()

    def expect_countdown_finished(self):
        expect(self._resend_code).to_be_visible(timeout=310000)
        expect(self._verify_button).to_be_enabled(timeout=310000)

    def expect_resend_countdown_is_not_started(self):
        expect(self._resend_code_countdown).not_to_be_visible()

    def expect_resent_code_is_available(self):
        expect(self._resend_code).to_be_visible()
