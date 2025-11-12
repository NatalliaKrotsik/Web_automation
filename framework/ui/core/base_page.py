from playwright.sync_api import Page

class BasePage():
    def __init__(self, page: Page, url: str):
        self.base_page = page
        self.url = url

    def open(self):
        self.base_page.goto(self.url)