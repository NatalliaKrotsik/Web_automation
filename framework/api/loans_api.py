import allure
import requests
from framework.api.core.http_client import HttpClient


class LoansAPI(HttpClient):
    def __init__(self, jwt_token: str):
        super().__init__(default_headers={"Authorization": f"JWT {jwt_token}"})
        self.endpoint = "loans/"

    @allure.step("Get all loans of an authorized user.")
    def get_all_loans_of_user(self) -> requests.Response:
        """
        Returns list of loans of an authorized user as a requests.Request.

        """
        return self.get(path=self.endpoint + "list/")

    @allure.step("Check creation of a new loan for a specific user.")
    def check_new_consumer_loan_creation(
        self, user_uuid: str, email: str
    ) -> requests.Response:
        """
        Checks creation of a new consumer loan of an authorized user
        and returns as a requests.Request.

        """
        data = {
            "user_uuid": user_uuid,
            "email": email,
            "total_repayment": 5000,
            "monthly_payment": 100,
            "amount": 1000,
            "loan_term": 6,
            "currency": "PLN",
            "loan_user_account": "Loan_User_New",
        }
        return self.post(path=self.endpoint, **data)
