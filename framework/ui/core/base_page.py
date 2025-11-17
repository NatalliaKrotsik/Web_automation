from framework.ui.core.base_element import BaseElement
from playwright.sync_api import Page

class BasePage():
    def __init__(self, page: Page, url: str):
        self.base_page = page
        self.url = url

    def open(self) -> None:
        self.base_page.goto(self.url)

    def find_element(self, selector: str) -> BaseElement:
        return BaseElement(self.base_page, selector)

    def find_all_elements(self, selector: str) -> list[BaseElement]:
        elems = self.page.locator(selector).all()
        return [BaseElement(self.page, f"{selector} >> nth={i}") for i in range(len(elems))]

    def wait_for_element(self, selector: str, timeout: int = 5000) -> BaseElement:
        element = BaseElement(self.base_page, selector)
        if element.is_visible():
            return element

    def wait_for_elements(self, selector: str, timeout: int = 15000):
        elements = self.base_page.query_selector_all(selector)
        if not elements:
            elements = self.base_page.wait_for_selector(
                selector, timeout=timeout
            )
        return elements

    def get_current_url(self) -> str:
        return self.base_page.url

    def wait_for_timeout(self, timeout_ms) -> None:
        self.base_page.wait_for_timeout(timeout_ms)

    def wait_for_the_url(self, url: str, timeout: int = 5000) -> None:
        self.base_page.wait_for_url(url, timeout=timeout)

    def context(self) -> Page:
        return self.base_page.context

    def get_data_from_clipboard(self) -> str:
        """Get data from the clipboard using a hidden element"""
        self.base_page.evaluate(
            """
            const hiddenTextarea = document.createElement('textarea');
            hiddenTextarea.setAttribute('id', 'hiddenTextarea');
            hiddenTextarea.style.position = 'fixed';
            hiddenTextarea.style.top = '-1000px';
            document.body.appendChild(hiddenTextarea);
            hiddenTextarea.focus();
        """
        )

        self.base_page.keyboard.press("Meta+V")

        clipboard_content = self.base_page.evaluate(
            "() => document.getElementById('hiddenTextarea').value"
        )
        return clipboard_content

    def refresh_page(self) -> None:
        self.base_page.reload()