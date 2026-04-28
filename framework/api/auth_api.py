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
            raise ValueError(
                f"Authorization failed with status code {auth.status_code}"
            )
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
