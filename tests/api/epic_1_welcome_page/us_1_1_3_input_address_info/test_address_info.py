import copy

import allure
import pytest
from assertpy import assert_that

from tests.api.epic_1_welcome_page.data.address_data import (
    invalid_apartments,
    invalid_cities,
    invalid_house_numbers,
    invalid_postal_codes,
    invalid_streets,
    postal_city_mismatch,
    valid_address,
)

pytestmark = [pytest.mark.api, pytest.mark.regression]


@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.3 Input Address Info")
class _AddressBase:
    """Shared Allure hierarchy for all address test classes."""


@allure.story("Registration address validation")
class TestRegistrationAddressValidation(_AddressBase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration street")
    @pytest.mark.parametrize("street", invalid_streets)
    def test_invalid_registration_street(self, address_api, street):
        with allure.step(f"Submit address with invalid street: {street!r}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["street"] = street
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid street must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration house number")
    @pytest.mark.parametrize("house_number", invalid_house_numbers)
    def test_invalid_registration_house_number(self, address_api, house_number):
        with allure.step(f"Submit address with invalid house number: {house_number!r}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["houseNumber"] = house_number
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid house number must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration apartment")
    @pytest.mark.parametrize("apartment", invalid_apartments)
    def test_invalid_registration_apartment(self, address_api, apartment):
        with allure.step(f"Submit address with invalid apartment: {apartment!r}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["apartment"] = apartment
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid apartment must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration postal code")
    @pytest.mark.parametrize("postal_code", invalid_postal_codes)
    def test_invalid_registration_postal_code(self, address_api, postal_code):
        with allure.step(f"Submit address with invalid postal code: {postal_code!r}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["postalCode"] = postal_code
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid postal code must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid registration city")
    @pytest.mark.parametrize("city", invalid_cities)
    def test_invalid_registration_city(self, address_api, city):
        with allure.step(f"Submit address with invalid city: {city!r}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["city"] = city
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid city must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send mismatched postal code and city")
    @pytest.mark.parametrize("mismatch", postal_city_mismatch)
    def test_postal_code_city_mismatch(self, address_api, mismatch):
        with allure.step(f"Submit address with mismatched postal/city: {mismatch}"):
            payload = copy.deepcopy(valid_address)
            payload["registrationAddress"]["postalCode"] = mismatch["postalCode"]
            payload["registrationAddress"]["city"] = mismatch["city"]
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Mismatched postal code and city must be rejected"
            ).is_in(400, 422)


@allure.story("Billing address validation")
class TestBillingAddressValidation(_AddressBase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing street when separate billing address enabled")
    @pytest.mark.parametrize("street", invalid_streets)
    def test_invalid_billing_street(self, address_api, street):
        with allure.step(f"Submit billing address with invalid street: {street!r}"):
            payload = copy.deepcopy(valid_address)
            payload["billingSameAsRegistration"] = False
            payload["billingAddress"]["street"] = street
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid billing street must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing house number when separate billing address enabled")
    @pytest.mark.parametrize("house_number", invalid_house_numbers)
    def test_invalid_billing_house_number(self, address_api, house_number):
        with allure.step(f"Submit billing address with invalid house number: {house_number!r}"):
            payload = copy.deepcopy(valid_address)
            payload["billingSameAsRegistration"] = False
            payload["billingAddress"]["houseNumber"] = house_number
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid billing house number must be rejected"
            ).is_in(400, 422)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send invalid billing postal code when separate billing address enabled")
    @pytest.mark.parametrize("postal_code", invalid_postal_codes)
    def test_invalid_billing_postal_code(self, address_api, postal_code):
        with allure.step(f"Submit billing address with invalid postal code: {postal_code!r}"):
            payload = copy.deepcopy(valid_address)
            payload["billingSameAsRegistration"] = False
            payload["billingAddress"]["postalCode"] = postal_code
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 400 or 422"):
            assert_that(response.status_code).described_as(
                "Invalid billing postal code must be rejected"
            ).is_in(400, 422)


@allure.story("Valid address submission")
class TestValidAddressSubmission(_AddressBase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send valid address with billingSameAsRegistration True")
    def test_valid_address_same_billing(self, address_api):
        with allure.step("Submit valid address with billingSameAsRegistration=True"):
            payload = copy.deepcopy(valid_address)
            payload["billingSameAsRegistration"] = True
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as(
                "Valid address should be accepted"
            ).is_equal_to(200)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Send valid address with billingSameAsRegistration False")
    def test_valid_address_different_billing(self, address_api):
        with allure.step("Submit valid address with separate billing address"):
            payload = copy.deepcopy(valid_address)
            payload["billingSameAsRegistration"] = False
            payload["billingAddress"]["type"] = "billing"
            response = address_api.submit_address(payload)
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as(
                "Valid address with separate billing should be accepted"
            ).is_equal_to(200)
