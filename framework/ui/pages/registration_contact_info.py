from playwright.sync_api import expect

from framework.ui.core.base_page import BasePage


class RegistrationPage(BasePage):

    def __init__(self, page):
        super().__init__(page, "https://dev.pretty-py.andersenlab.dev/sign-up")
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

    def open(self):
        self.page.goto("https://dev.pretty-py.andersenlab.dev/sign-up")

    def fill_personal_information_step_with_valid_data(self):
        self._first_name_input.fill("Alina")
        self._middle_name_input.fill("Petrovna")
        self._last_name_input.fill("Petrova")
        self._passport_id_input.fill("123456789")
        self._birth_date_input.click()
        self.page.get_by_role("button", name="2", exact=True).click()

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
