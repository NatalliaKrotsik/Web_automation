import allure
import pytest


@pytest.mark.ui
@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestDuplicatePassport:

    @allure.title("TC-62 — Duplicate passport ID shows error in UI")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_duplicate_passport_shows_error(self, page):
        pass
