from urllib import request
import pytest
from framework.ui.core.browser_manager import BrowserManager

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode"
    )

@pytest.fixture(scope="session")
def page():
    browser_type = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    bm = BrowserManager(browser_type=browser_type, headless=headless)
    page = bm.start()
    yield page
    bm.stop()