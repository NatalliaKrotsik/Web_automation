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
