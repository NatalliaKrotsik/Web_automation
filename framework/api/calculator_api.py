import allure
import requests

from framework.api.core.http_client import HttpClient


class CalculatorAPI(HttpClient):
    """API client for exchange-rate calculator (US-1.17)."""

    def __init__(self):
        super().__init__()
        self.endpoint = "api/processing-center/exchange-rates/calculate"

    @allure.step("Calculate exchange amount")
    def calculate(
        self,
        sell_currency: str | None,
        get_currency: str | None,
        sell_amount: float | None,
        get_amount: float | None,
    ) -> requests.Response:
        return self.post(
            path=self.endpoint,
            json_body={
                "sellCurrency": sell_currency,
                "getCurrency": get_currency,
                "sellAmount": sell_amount,
                "getAmount": get_amount,
            },
        )
