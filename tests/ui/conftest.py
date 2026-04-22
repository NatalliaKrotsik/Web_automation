import pytest
from framework.env_manager import EnvManager
from framework.ui.core.browser_manager import BrowserManager


@pytest.fixture(scope="session")
def page():
    ui_config = EnvManager.get_config()["ui"]
    bm = BrowserManager(
        browser_type=ui_config.get("browser", "chromium"),
        headless=ui_config.get("headless", True),
        slow_mo=ui_config.get("slow_mo", 0)
    )
    page = bm.start()
    yield page
    bm.stop()
