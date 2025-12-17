import allure 
import requests
from framework.api.core.http_client import HttpClient 

class AuthAPI(HttpClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "auth/"
        self.__access_token = None
        self.__refresh_token = None
        self.__id_token = None

    @property
    def access_token(self):
        return self.__access_token
    
    @property
    def refresh_token(self):
        return self.__refresh_token
    
    @property
    def id_token(self):
        return self.__id_token
    
    @allure.step('Authorization step')
    def authorization(self, email: str, password: str) -> requests.Response:
        data = {
            "email": email,
            "password": password
        }
        auth = self.post(path=self.endpoint + 'sign-in/', json_body=data)
        if auth.status_code != 200:
            raise ValueError(f'Authorization failed with status code {auth.status_code}')
        tokens = auth.json()
        auth_headers = {'Authorization': f'JWT {tokens.get("id_token")}'}
        self.update_headers(auth_headers)
        self.__access_token = tokens.get("access_token")
        self.__refresh_token = tokens.get("refresh_token")
        self.__id_token = tokens.get("id_token")
        return auth

    
    @allure.step("User logout step.")
    def sign_out_user(self, refresh_token: str) -> requests.Response:
        """
        Sign out user by using refresh token.

        """
        return self.post(
            path=self.endpoint + "sign-out/", 
            json_body={"refresh": refresh_token}
            )