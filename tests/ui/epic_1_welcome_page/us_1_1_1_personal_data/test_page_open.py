import allure
import pytest

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestPageOpen:

    @allure.title("TC-02 — Sign Up opens Personal Info form")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sign_up_opens_personal_info_form(self, page):
        pass