import allure

from framework.api.core.http_client import HttpClient


class TemporaryPasswordAPI(HttpClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "api/auth/send-temporary-password"

    @allure.step("Send temporary password")
    def send_temporary_password(self):
        return self.post(path=self.endpoint, json_body={"email": "pretty2.aqa@gmail.com"})
