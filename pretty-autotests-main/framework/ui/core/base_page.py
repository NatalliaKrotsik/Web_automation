from framework.ui.core.base_element import BaseElement
from playwright.sync_api import Page

class BasePage():
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url

    def open(self) -> None:
        self.page.goto(self.url)

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_timeout(self, timeout_ms) -> None:
        self.page.wait_for_timeout(timeout_ms)

    def wait_for_the_url(self, url: str, timeout: int = 5000) -> None:
        self.page.wait_for_url(url, timeout=timeout)

    def context(self) -> Page:
        return self.page.context

    def get_data_from_clipboard(self) -> str:
        """Get data from the clipboard using a hidden element"""
        self.page.evaluate(
            """
            const hiddenTextarea = document.createElement('textarea');
            hiddenTextarea.setAttribute('id', 'hiddenTextarea');
            hiddenTextarea.style.position = 'fixed';
            hiddenTextarea.style.top = '-1000px';
            document.body.appendChild(hiddenTextarea);
            hiddenTextarea.focus();
        """
        )

        self.page.keyboard.press("Meta+V")

        clipboard_content = self.page.evaluate(
            "() => document.getElementById('hiddenTextarea').value"
        )
        return clipboard_content

    def refresh_page(self) -> None:
        self.page.reload()