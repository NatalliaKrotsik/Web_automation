import allure
import pytest


@pytest.mark.ui
@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class TestDataPersistence:

    @allure.title("TC-76 — Back navigation preserves entered data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_navigation_preserves_data(self, page):
        pass

    @allure.title("TC-77 — Re-validation triggers on return to form")
    @allure.severity(allure.severity_level.NORMAL)
    def test_revalidation_on_return(self, page):
        pass
