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

    def wait_for_elements(self, timeout: int = 15000):
        elements = self.page.locator(self.selector).all()
        if not elements:
            elements = self.page.wait_for_selector(
                self.selector, timeout=timeout
            )
        return elements
    
    def find_element(self) -> None:
        return BaseElement(self.page, self.selector)

    def find_all_elements(self) -> list:
        elems = self.page.locator(self.selector).all()
        return [BaseElement(self.page, f"{self.selector} >> nth={i}") for i in range(len(elems))]