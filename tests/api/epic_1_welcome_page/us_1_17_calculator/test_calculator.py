import allure
import pytest
import requests

from tests.api.epic_1_welcome_page.data.calculator_data import (
    INVALID_CALCULATOR_DATA,
    VALID_CALCULATOR_DATA,
)

BASE_URL = "https://api-dev.pretty-py.andersenlab.dev"


def calculate_exchange(
    sell_currency,
    get_currency,
    sell_amount,
    get_amount,
):
    return requests.post(
        f"{BASE_URL}/api/processing-center/exchange-rates/calculate",
        json={
            "sellCurrency": sell_currency,
            "getCurrency": get_currency,
            "sellAmount": sell_amount,
            "getAmount": get_amount,
        },
    )


@allure.epic("API")
@allure.feature("Exchange Calculator")
class TestExchangeCalculator:

    @allure.title("Calculate exchange amount with valid data")
    @pytest.mark.parametrize(
        "sell_currency, get_currency, sell_amount, get_amount",
        VALID_CALCULATOR_DATA,
    )
    def test_calculate_exchange_with_valid_data(
        self,
        sell_currency,
        get_currency,
        sell_amount,
        get_amount,
    ):
        response = calculate_exchange(
            sell_currency,
            get_currency,
            sell_amount,
            get_amount,
        )

        assert response.status_code == 200

        body = response.json()

        assert body["sellCurrency"] == sell_currency
        assert body["getCurrency"] == get_currency

        if sell_amount is not None:
            assert body["sellAmount"] == sell_amount
            assert body["getAmount"] is not None

        if get_amount is not None:
            assert body["getAmount"] == get_amount
            assert body["sellAmount"] is not None

    @allure.title("Exchange calculator validation errors")
    @pytest.mark.parametrize(
        "sell_currency, get_currency, sell_amount, get_amount, expected_status, expected_error",
        INVALID_CALCULATOR_DATA,
    )
    def test_exchange_calculator_validation_errors(
        self,
        sell_currency,
        get_currency,
        sell_amount,
        get_amount,
        expected_status,
        expected_error,
    ):
        response = calculate_exchange(
            sell_currency,
            get_currency,
            sell_amount,
            get_amount,
        )

        assert response.status_code == expected_status

        body = response.json()

        assert expected_error in str(body)
