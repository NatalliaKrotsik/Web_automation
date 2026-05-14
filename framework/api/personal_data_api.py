import allure
import requests
from framework.api.core.http_client import HttpClient


class PersonalDataAPI(HttpClient):
    """API client for the personal-info registration step (US-1.1.1)."""

    def __init__(self):
        super().__init__()
        self.endpoint = "api/registration/personal-info"

    @allure.step("Submit personal info")
    def submit_personal_info(
        self,
        first_name: str,
        last_name: str,
        passport_id: str,
        birth_date: str,
        middle_name: str | None = None,
    ) -> requests.Response:
        payload = {
            "firstName":  first_name,
            "lastName":   last_name,
            "passportId": passport_id,
            "birthDate":  birth_date,
        }
        if middle_name is not None:
            payload["middleName"] = middle_name

        return self.post(path=self.endpoint, json_body=payload)