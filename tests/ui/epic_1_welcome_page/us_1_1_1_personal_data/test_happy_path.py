import allure
import pytest


@pytest.mark.ui
@pytest.mark.smoke
@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestHappyPath:

    @allure.title("TC-01 — Full valid submission completes registration step")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_full_valid_submission(self, page):
        pass
