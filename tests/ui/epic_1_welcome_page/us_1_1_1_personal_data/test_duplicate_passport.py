import allure
import pytest

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure hierarchy for personal info test classes."""


@allure.story("Duplicate passport")
class TestDuplicatePassport(_PersonalInfoBase):

    @allure.title("TC-62 — Duplicate passport ID shows error in UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Not implemented yet")
    def test_duplicate_passport_shows_error(self, page):
        pass
