import copy

import allure
import pytest
from assertpy import assert_that

from framework.api.address_api import AddressAPI
from tests.api.epic_1_welcome_page.data.address_data import (
    invalid_apartments,
    invalid_cities,
    invalid_house_numbers,
    invalid_postal_codes,
    invalid_streets,
    postal_city_mismatch,
    valid_address,
)


@pytest.mark.api
@allure.suite("API Tests - Address")
class TestAddressAPI:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration street")
    @pytest.mark.parametrize("street", invalid_streets)
    def test_invalid_registration_street(
        self,
        auth_tokens,
        street,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["street"] = street

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration house number")
    @pytest.mark.parametrize("house_number", invalid_house_numbers)
    def test_invalid_registration_house_number(
        self,
        auth_tokens,
        house_number,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["houseNumber"] = house_number

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration apartment")
    @pytest.mark.parametrize("apartment", invalid_apartments)
    def test_invalid_registration_apartment(
        self,
        auth_tokens,
        apartment,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["apartment"] = apartment

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration postal code")
    @pytest.mark.parametrize("postal_code", invalid_postal_codes)
    def test_invalid_registration_postal_code(
        self,
        auth_tokens,
        postal_code,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["postalCode"] = postal_code

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration city")
    @pytest.mark.parametrize("city", invalid_cities)
    def test_invalid_registration_city(
        self,
        auth_tokens,
        city,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["city"] = city

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send mismatched postal code and city")
    @pytest.mark.parametrize("mismatch", postal_city_mismatch)
    def test_postal_code_city_mismatch(
        self,
        auth_tokens,
        mismatch,
    ):
        payload = copy.deepcopy(valid_address)
        payload["registrationAddress"]["postalCode"] = mismatch["postalCode"]
        payload["registrationAddress"]["city"] = mismatch["city"]

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    # Tests for billing address when billingSameAsRegistration is False
    # According to Scenario 5: Uncheck billing = registration
    # When checkbox is unchecked, billing address must be validated separately

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing street when separate billing address enabled")
    @pytest.mark.parametrize("street", invalid_streets)
    def test_invalid_billing_street(
        self,
        auth_tokens,
        street,
    ):
        payload = copy.deepcopy(valid_address)
        payload["billingSameAsRegistration"] = False
        payload["billingAddress"]["street"] = street

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing house number when separate billing address enabled")
    @pytest.mark.parametrize("house_number", invalid_house_numbers)
    def test_invalid_billing_house_number(
        self,
        auth_tokens,
        house_number,
    ):
        payload = copy.deepcopy(valid_address)
        payload["billingSameAsRegistration"] = False
        payload["billingAddress"]["houseNumber"] = house_number

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing postal code when separate billing address enabled")
    @pytest.mark.parametrize("postal_code", invalid_postal_codes)
    def test_invalid_billing_postal_code(
        self,
        auth_tokens,
        postal_code,
    ):
        payload = copy.deepcopy(valid_address)
        payload["billingSameAsRegistration"] = False
        payload["billingAddress"]["postalCode"] = postal_code

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send valid address with billingSameAsRegistration True")
    def test_valid_address_same_billing(
        self,
        auth_tokens,
    ):
        """
        Scenario 4 & 6: When billingSameAsRegistration is True,
        billing address is automatically filled with registration address values
        """
        payload = copy.deepcopy(valid_address)
        payload["billingSameAsRegistration"] = True

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_equal_to(200)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send valid address with billingSameAsRegistration False")
    def test_valid_address_different_billing(
        self,
        auth_tokens,
    ):
        """
        Scenario 5: When billingSameAsRegistration is False,
        billing address must be filled separately and validated
        """
        payload = copy.deepcopy(valid_address)
        payload["billingSameAsRegistration"] = False
        # Billing address has same valid values
        payload["billingAddress"]["type"] = "billing"

        access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
        address_api = AddressAPI()
        address_api.update_headers({"Authorization": f"Bearer {access_token}"})

        response = address_api.submit_address(payload)

        assert_that(response.status_code).is_equal_to(200)
