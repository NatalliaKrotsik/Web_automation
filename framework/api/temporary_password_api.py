import allure
import yaml

from framework.api.core.http_client import HttpClient

with open("tests/api/epic_1_welcome_page/data/test_temporary_password.yaml", encoding="utf-8") as f:
    email = yaml.safe_load(f)["emails"]


class TemporaryPasswordAPI(HttpClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "api/auth/send-temporary-password"

    @allure.step("Send temporary password")
    def send_temporary_password(self):
        return self.post(path=self.endpoint, json_body={"email": email["test_user_email"]})
