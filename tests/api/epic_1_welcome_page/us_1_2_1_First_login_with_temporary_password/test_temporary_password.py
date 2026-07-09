import allure
import pytest
import yaml
from assertpy import assert_that

from framework.api.temporary_password_api import TemporaryPasswordAPI
from framework.email.email_verification_client import EmailVerification
from framework.env_manager import EnvManager

pytestmark = [pytest.mark.api]


@allure.parent_suite("API tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.2.1 First login with temporary password")
class _TemporaryPasswordBase:
    pass


@allure.story("Sent temporary password")
@pytest.mark.qase("LP-211")
class TestTemporaryPassword(_TemporaryPasswordBase):
    @pytest.fixture(scope="function", autouse=True)
    def test_emails(self):
        with open(
            "tests/api/epic_1_welcome_page/data/test_temporary_password.yaml",
            encoding="utf-8",
        ) as f:
            return yaml.safe_load(f)

    @pytest.fixture(scope="function", autouse=True)
    def temporary_password(self, test_emails):
        sender = TemporaryPasswordAPI()
        sender.send_temporary_password()
        EMAIL = test_emails["emails"]["test_user_email"]
        PASSWORD = EnvManager.get("IMAP_PASSWORD")
        email_helper = EmailVerification(EMAIL, PASSWORD)
        email_helper.connect()
        code = email_helper.get_verification_code(sender_email=test_emails["emails"]["sender_email"])
        yield code
        email_helper.disconnect()

    @pytest.mark.skip("Because of email essue")
    def test_if_temporary_password_was_sent(self, temporary_password):
        assert_that(temporary_password).described_as("Expected to be sent").is_not_none()
