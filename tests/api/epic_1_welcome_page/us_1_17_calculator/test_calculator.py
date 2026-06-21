import allure
import pytest
from assertpy import assert_that

from tests.api.epic_1_welcome_page.data.calculator_data import (
    INVALID_CALCULATOR_DATA,
    VALID_CALCULATOR_DATA,
)

pytestmark = [pytest.mark.api, pytest.mark.regression]


@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.17 Exchange Calculator")
class _CalculatorBase:
    """Shared Allure hierarchy for all calculator test classes."""


@allure.story("Valid calculation")
@pytest.mark.qase("LP-230")
class TestValidCalculation(_CalculatorBase):
    test_data_map = {"calc_case": VALID_CALCULATOR_DATA}

    @allure.title("Calculate exchange amount with valid data — {calc_case}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_calculate_exchange_with_valid_data(self, calculator_api, calc_case):
        with allure.step(
            f"POST calculate: {calc_case['sell_currency']} → {calc_case['get_currency']}, "
            f"sell={calc_case['sell_amount']}, get={calc_case['get_amount']}"
        ):
            response = calculator_api.calculate(
                sell_currency=calc_case["sell_currency"],
                get_currency=calc_case["get_currency"],
                sell_amount=calc_case["sell_amount"],
                get_amount=calc_case["get_amount"],
            )
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as(
                f"Expected 200 for case {calc_case['name']!r}"
            ).is_equal_to(200)
        with allure.step("Assert response currencies match request"):
            body = response.json()
            assert_that(body["sellCurrency"]).described_as(
                "sellCurrency in response must match request"
            ).is_equal_to(calc_case["sell_currency"])
            assert_that(body["getCurrency"]).described_as(
                "getCurrency in response must match request"
            ).is_equal_to(calc_case["get_currency"])
        with allure.step("Assert computed amount is present"):
            if calc_case["sell_amount"] is not None:
                assert_that(body["sellAmount"]).described_as(
                    "sellAmount must equal request value"
                ).is_equal_to(calc_case["sell_amount"])
                assert_that(body["getAmount"]).described_as(
                    "getAmount must be computed (not None)"
                ).is_not_none()
            if calc_case["get_amount"] is not None:
                assert_that(body["getAmount"]).described_as(
                    "getAmount must equal request value"
                ).is_equal_to(calc_case["get_amount"])
                assert_that(body["sellAmount"]).described_as(
                    "sellAmount must be computed (not None)"
                ).is_not_none()


@allure.story("Validation errors")
@pytest.mark.qase("LP-231")
class TestCalculatorValidationErrors(_CalculatorBase):
    test_data_map = {"calc_case": INVALID_CALCULATOR_DATA}

    @allure.title("Exchange calculator returns validation error — {calc_case}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_exchange_calculator_validation_errors(self, calculator_api, calc_case):
        with allure.step(
            f"POST calculate with invalid data: {calc_case['sell_currency']} → {calc_case['get_currency']}"
        ):
            response = calculator_api.calculate(
                sell_currency=calc_case["sell_currency"],
                get_currency=calc_case["get_currency"],
                sell_amount=calc_case["sell_amount"],
                get_amount=calc_case["get_amount"],
            )
        with allure.step(f"Assert status code is {calc_case['expected_status']}"):
            assert_that(response.status_code).described_as(
                f"Expected {calc_case['expected_status']} for case {calc_case['name']!r}"
            ).is_equal_to(calc_case["expected_status"])
        with allure.step(f"Assert error message: {calc_case['expected_error']!r}"):
            assert_that(str(response.json())).described_as(
                "Response must contain expected error text"
            ).contains(calc_case["expected_error"])
