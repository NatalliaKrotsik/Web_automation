import allure
import requests

from framework.api.core.http_client import HttpClient


class ExchangeRatesAPI(HttpClient):
    """API client for exchange rates (US-1.15)."""

    def __init__(self):
        super().__init__()
        self.endpoint = "api/processing-center/exchange-rates"  # was: api/exchange-rates

    @allure.step("Get exchange rates")
    def get_exchange_rates(self) -> requests.Response:
        return self.get(path=self.endpoint)