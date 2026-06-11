import allure
import pytest
import requests

from tests.api.epic_1_welcome_page.data.log_into_my_profile_data import (
    INVALID_SIGN_IN_DATA,
    VALID_SIGN_IN_DATA,
)

BASE_URL = "https://api-dev.pretty-py.andersenlab.dev"


def sign_in(email, password):
    return requests.post(
        f"{BASE_URL}/api/auth/sign-in",
        json={
            "email": email,
            "password": password,
        },
    )


@allure.epic("API")
@allure.feature("Sign In")
class TestSignIn:

    @allure.title("Sign in with valid credentials")
    @pytest.mark.parametrize(
        "email, password, expected_status",
        VALID_SIGN_IN_DATA,
    )
    def test_sign_in_with_valid_credentials(
        self,
        email,
        password,
        expected_status,
    ):
        assert expected_status == 200

    @allure.title("Sign in with invalid credentials")
    @pytest.mark.parametrize(
        "email, password, expected_error, expected_status",
        INVALID_SIGN_IN_DATA,
    )
    def test_sign_in_with_invalid_credentials(
        self,
        email,
        password,
        expected_error,
        expected_status,
    ):
        assert expected_status in [400, 401, 409, 422]

    @allure.title("User is blocked after 5 invalid sign-in attempts")
    def test_user_is_blocked_after_5_invalid_attempts(self):
        for _ in range(5):
            response = sign_in(
                email="test@test.com",
                password="wrong_password",
            )
            assert response.status_code == 401

        response = sign_in(
            email="xonib78658@inreur.com",
            password="Aa12345!",
        )

        assert response.status_code == 423
