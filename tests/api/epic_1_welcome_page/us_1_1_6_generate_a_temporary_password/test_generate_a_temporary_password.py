import time

import allure
import pytest
from assertpy import assert_that

from framework.api.auth_api import AuthAPI
from tests.api.epic_1_welcome_page.data.address_data import valid_address

pytestmark = [pytest.mark.api]


@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.1.6 Generate a temporary password")
class _GenerateTemporaryPassword:
    """Shared Allure labels for all exchange rate test classes."""


@allure.story("Verify temporary profile and temporary password are created after successful sign-up")
@pytest.mark.qase("LP-452")
class TestGenerateTemporaryPassword(_GenerateTemporaryPassword):

    @pytest.fixture(scope="function", autouse=True)
    def _setup(self, db_client):
        auth_api = AuthAPI()

        unique_id = int(time.time())
        dynamic_email = f"alina.petrova_{unique_id}@gmail.com"
        dynamic_phone = f"+482999{str(unique_id)[-5:]}"

        payload = {
            "addresses": [valid_address["registrationAddress"]],
            "billingSameAsRegistration": True,
            "agreements": [
                {"type": "BANKING_AGREEMENT", "version": "v1"},
                {"type": "PRIVACY_POLICY_AND_TERMS_OF_USE", "version": "v1"},
            ],
            "contact": {"email": dynamic_email, "phone": dynamic_phone},
            "personalInfo": {
                "firstName": "Ivan",
                "lastName": "Pavel",
                "middleName": "Petrov",
                "passportId": f"BR25{str(unique_id)[-5:]}",
                "birthDate": "01\\01\\1990",
            },
        }

        with allure.step("POST /api/auth/sign-up"):
            self.response = auth_api.sign_up(
                addresses=payload["addresses"],
                billing_same_as_registration=payload["billingSameAsRegistration"],
                agreements=payload["agreements"],
                contact=payload["contact"],
                personal_info=payload["personalInfo"],
            )
        self.user_id = self.response.json().get("userId") if self.response.status_code == 201 else None
        self.email = dynamic_email
        self.db_client = db_client
        print(f"Status: {self.response.status_code}")
        print(f"Body: {self.response.text}")

    @allure.title("Status code is 201 Created")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_status_code_is_201(self):
        assert_that(self.response.status_code).described_as("Status code").is_equal_to(201)

    @allure.title("Response body contains userID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_response_contains_user_id(self):
        self.body = self.response.json()
        assert_that(self.body).described_as("Response body").contains_key("userId")

    @allure.title("User exist in database with correct email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_exist_in_database_with_correct_email(self):
        user = self.db_client.get_user_data(email=self.email)
        assert_that(user).described_as("User in database").is_not_none()
        assert_that(user.email).described_as("User email").is_equal_to(self.email)
