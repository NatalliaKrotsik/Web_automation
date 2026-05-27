import allure
import pytest
from assertpy import assert_that

from framework.api.address_api import AddressAPI
from tests.api.epic_1_welcome_page.data.address_data import valid_address


@pytest.mark.api
@allure.suite("API Tests - Address")
class TestAddressAPI:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send address info")
    def test_address_info(self, auth_tokens):
        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})
        response = address_api.submit_address(valid_address)
        assert_that(response.status_code).is_equal_to(200)
