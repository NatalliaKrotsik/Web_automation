import allure
import pytest


@pytest.mark.ui
@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestFieldValidationVisual:

    @allure.title("TC-03 — Submit button disabled until all required fields filled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_button_disabled_when_form_empty(self, page):
        pass

    @allure.title("TC-04 — Required field messages shown on empty submit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_required_field_messages_shown(self, page):
        pass

    @allure.title("TC-66 — Non-numeric input rejected in birth date field")
    @allure.severity(allure.severity_level.NORMAL)
    def test_non_numeric_birth_date_rejected(self, page):
        pass
