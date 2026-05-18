import allure
import pytest


@pytest.mark.ui
@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestDataLoss:

    @allure.title("TC-78 — Page reload clears unsaved form data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reload_clears_form_data(self, page):
        pass

    @allure.title("TC-79 — Closing tab loses unsaved form data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_tab_loses_form_data(self, page):
        pass
