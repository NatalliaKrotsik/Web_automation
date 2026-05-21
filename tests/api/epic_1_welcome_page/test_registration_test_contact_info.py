import allure
import pytest
import requests

from tests.api.epic_1_welcome_page.data.registration_test_contact_info_data import (
    INVALID_EMAILS,
    INVALID_PHONES,
    VALID_EMAILS,
    VALID_PHONES,
)


class TestRegistrationContactInfoAPI:
    BASE_URL = "https://api-dev.pretty-py.andersenlab.dev"

    ENDPOINT = "/api/registration/contact-info"

    URL = f"{BASE_URL}{ENDPOINT}"

    @allure.title("API accepts valid email")
    @pytest.mark.parametrize("data", VALID_EMAILS)
    def test_api_accepts_valid_email(self, data):

        response = requests.post(self.URL, json=data, timeout=5)

        assert response.status_code == 201

    @allure.title("API rejects invalid email")
    @pytest.mark.parametrize("data", INVALID_EMAILS)
    def test_api_rejects_invalid_email(self, data):

        response = requests.post(self.URL, json=data)

        assert response.status_code == 422

    @allure.title("API accepts valid phone")
    @pytest.mark.parametrize("data", VALID_PHONES)
    def test_api_accepts_valid_phone(self, data):

        response = requests.post(self.URL, json=data)

        assert response.status_code == 201

    @allure.title("API rejects invalid phone")
    @pytest.mark.parametrize("data", INVALID_PHONES)
    def test_api_rejects_invalid_phone(self, data):

        response = requests.post(self.URL, json=data)

        assert response.status_code == data["expected_status"]
