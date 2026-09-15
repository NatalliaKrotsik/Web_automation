class SignInLocators:
    LOGIN_NAV_BUTTON = 'a[href="/login"] button'

    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"

    LOGIN_BUTTON = 'button[type="submit"]'

    VALIDATION_ERROR = "span.text-text-errorBody"
    GENERAL_ERROR = "div.bg-labels-red"


class SignInPage:

    def __init__(self, page):
        self.page = page

    def open_sign_in_page(self):
        self.page.locator(SignInLocators.LOGIN_NAV_BUTTON).click()

    def fill_email(self, email):
        self.page.locator(SignInLocators.EMAIL_INPUT).fill(email)

    def fill_password(self, password):
        self.page.locator(SignInLocators.PASSWORD_INPUT).fill(password)

    def click_login(self):
        self.page.locator(SignInLocators.LOGIN_BUTTON).click()

    def clear_email(self):
        self.page.locator(SignInLocators.EMAIL_INPUT).fill("")

    def clear_password(self):
        self.page.locator(SignInLocators.PASSWORD_INPUT).fill("")

    def click_email_field(self):
        self.page.locator(SignInLocators.EMAIL_INPUT).click()

    def click_password_field(self):
        self.page.locator(SignInLocators.PASSWORD_INPUT).click()

    # Expects

    def expect_login_button_enabled(self):
        from playwright.sync_api import expect
        expect(self.page.locator(SignInLocators.LOGIN_BUTTON)).to_be_enabled()

    def expect_login_button_disabled(self):
        from playwright.sync_api import expect
        expect(self.page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()

    def expect_validation_error_contains(self, text: str):
        from playwright.sync_api import expect
        expect(self.page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text(text)

    def expect_general_error_contains(self, text: str):
        from playwright.sync_api import expect
        expect(self.page.locator(SignInLocators.GENERAL_ERROR)).to_contain_text(text)

    def expect_url_is_login(self, base_url: str):
        from playwright.sync_api import expect
        expect(self.page).to_have_url(f"{base_url}/login")

    def expect_url_is_not_login(self, base_url: str):
        from playwright.sync_api import expect
        expect(self.page).not_to_have_url(f"{base_url}/login")
