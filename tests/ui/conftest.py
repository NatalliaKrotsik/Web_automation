from urllib import request
import pytest
from framework.ui.core.browser_manager import BrowserManager

@pytest.fixture(scope="session")
def page():
    bm = BrowserManager(browser_type="chromium")
    page = bm.start()
    yield page
    bm.stop()