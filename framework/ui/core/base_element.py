from playwright.sync_api import Locator, Page


class BaseElement():
    def __init__(self, page: Page, selector: str):
        self.page = page
        self.selector = selector
        self.locator: Locator = page.locator(selector)

    def is_visible(self) -> bool:
        try:
            self.locator.wait_for(state="visible", timeout=5000)
            return True
        except:
            return False
        
    def click(self) -> None:
        self.page.wait_for_selector(self.selector, state="visible")
        self.locator.click()

    def wait_for_visible(self, timeout: int = 5000) -> None:
        self.locator.wait_for(state="visible", timeout=timeout)

    def get_text(self) -> str:
        self.wait_for_visible()
        return self.locator.inner_text()
    
    def hover(self) -> None:
        self.wait_for_visible()
        self.locator.hover()