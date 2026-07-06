import allure
import requests

from framework.api.core.http_client import HttpClient


class AuthAPI(HttpClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "api/auth/"
        self.__access_token = None
        self.__refresh_token = None

    @allure.step("Authorization step")
    def authorization(self, email: str, password: str) -> requests.Response:
        data = {"email": email, "password": password}
        auth = self.post(path=self.endpoint + "sign-in", json_body=data)
        if auth.status_code != 200:
            raise ValueError(f"Authorization failed with status code {auth.status_code}")
        tokens = auth.json()
        authentication_result = tokens.get("authenticationResult", {})
        auth_headers = {"Authorization": f'Bearer {authentication_result.get("accessToken")}'}
        self.update_headers(auth_headers)
        self.__access_token = authentication_result.get("accessToken")
        self.__refresh_token = authentication_result.get("refreshToken")
        return auth

    @allure.step("User logout step.")
    def sign_out_user(self, access_token: str) -> requests.Response:
        return self.post(path=self.endpoint + "sign-out", json_body={"accessToken": access_token})

    @allure.step("Session ping step")
    def session_ping(self, access_token: str) -> requests.Response:
        return self.post(path=self.endpoint + "session/ping", json_body={"accessToken": access_token})

    @allure.step("User sign up")
    def sign_up(
        self, personal_info: dict, contact: dict, addresses: list, agreements: list, billing_same_as_registration: bool
    ) -> requests.Response:
        data = {
            "personalInfo": personal_info,
            "contact": contact,
            "addresses": addresses,
            "agreements": agreements,
            "billingSameAsRegistration": billing_same_as_registration,
        }
        return self.post(path=self.endpoint + "sign-up", json_body=data)
