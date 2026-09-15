import allure
import pytest

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure hierarchy for personal info test classes."""


@allure.story("Happy path")
class TestHappyPath(_PersonalInfoBase):

    @allure.title("TC-01 — Full valid submission completes registration step")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.skip(reason="Not implemented yet")
    def test_full_valid_submission(self, page):
        pass
