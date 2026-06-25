import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.address_page import AddressLocators

pytestmark = [pytest.mark.ui]

VALID_ADDRESS = {
    "street": "Prosta",
    "house_number": "1",
    "apartment": "15",
    "postal_code": "00-001",
    "city": "Warszawa",
}


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.3 Address Info")
class TestHappyPath:

    @allure.title("TC-01 — All address fields accept valid values and Continue becomes clickable")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_full_valid_submission(self, address_page):
        address_page.fill_registration_address(**VALID_ADDRESS)
        address_page.check_billing_same_as_registration()

        expect(address_page.page.locator(AddressLocators.REGISTRATION_STREET)).to_have_value(VALID_ADDRESS["street"])
        expect(address_page.page.locator(AddressLocators.REGISTRATION_HOUSE_NUMBER)).to_have_value(
            VALID_ADDRESS["house_number"]
        )
        expect(address_page.page.locator(AddressLocators.REGISTRATION_APARTMENT)).to_have_value(
            VALID_ADDRESS["apartment"]
        )
        expect(address_page.page.locator(AddressLocators.REGISTRATION_POSTAL_CODE)).to_have_value(
            VALID_ADDRESS["postal_code"]
        )
        expect(address_page.page.locator(AddressLocators.CONTINUE_BUTTON)).to_be_enabled()

        address_page.click_continue()
