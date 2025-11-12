from abc import ABC
from playwright.sync_api import Locator, Page


class BaseElement(ABC):
    def __init__(self, page: Page, selector: str):
        self.page = page
        self.selector = selector
        self.locator: Locator = page.locator(selector)

    def click(self) -> None:
        self.page.wait_for_selector(self.selector, state="attached")
        self.locator.click()

    def wait_for_visible(self, timeout: int = 5000) -> None:
        self.locator.wait_for(state="visible", timeout=timeout)

    def get_text(self) -> str:
        self.wait_for_visible()
        return self.locator.inner_text()