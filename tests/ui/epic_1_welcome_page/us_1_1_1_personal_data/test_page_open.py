import allure
import pytest

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure hierarchy for personal info test classes."""


@allure.story("Page open")
class TestPageOpen(_PersonalInfoBase):

    @allure.title("TC-02 — Sign Up opens Personal Info form")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Not implemented yet")
    def test_sign_up_opens_personal_info_form(self, page):
        pass
