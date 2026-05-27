import allure
import requests

from framework.api.core.http_client import HttpClient


class AddressAPI(HttpClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "api/registration/address"

    @allure.step("Submit registration and billing address")
    def submit_address(self, payload: dict) -> requests.Response:
        return self.post(path=self.endpoint, json_body=payload)
