from framework.ui.core.base_page import BasePage
from framework.ui.elements.button import Button
from dotenv import load_dotenv

load_dotenv()

import os

class ExamplePage(BasePage):

    SIGN_UP_BTN = '//a[@href="/signup"]'
    LOGIN_BTN = '//a[@href="/login"]'
    LOGO = "//*[@id='root']/div/header/div/div[1]/a"

    def __init__(self, page):
        super().__init__(page, os.getenv("BASE_URL_DEV"))
        self.page = page
        self.logo = page.locator(self.LOGO)
        self.login_btn = Button(page,self.LOGIN_BTN)
        self.signup_btn = Button(page,self.SIGN_UP_BTN)

    def click_logo(self):
        self.logo.click()

    def click_log_in(self):
        self.login_btn.click()

    def click_sign_up(self):
        self.signup_btn.click()