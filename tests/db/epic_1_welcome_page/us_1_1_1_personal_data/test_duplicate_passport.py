import allure
import pytest
from assertpy import assert_that

pytestmark = [pytest.mark.db, pytest.mark.regression]


@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    pass


@allure.story("Duplicate Passport ID")
@pytest.mark.qase("LP-327")
class TestDuplicatePassport(_PersonalInfoBase):
    """LP-327 — Submitting a passport ID already registered in the system returns a conflict error."""

    @allure.title("Duplicate passport ID — system returns conflict error")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_duplicate_passport_rejected(self, api, valid_payload):
        with allure.step("Submit personal info once to register passport ID"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                "First submission should return 201"
            ).is_equal_to(201)
        with allure.step("Submit same passport ID again — assert conflict"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                "Duplicate passport should be rejected"
            ).is_in(409, 422)
            error_messages = [
                m["message"]
                for errors in r.json().get("details", {}).values()
                for m in errors
            ]
            assert_that(error_messages).described_as(
                "Response must contain duplicate passport error text"
            ).contains("User profile with this passport ID already exists. Enter another passport ID or log in")

    @pytest.mark.skip(reason="Co-owner rules not testable yet — pending US-3.8 implementation")
    @allure.title("Duplicate passport ID — co-owner rules allow reuse")
    @allure.severity(allure.severity_level.NORMAL)
    def test_coowner_can_reuse_passport(self, api, valid_payload):
        """LP-327 Step 2 — co-owner scenario, untestable as of 06.04.2026."""
        pass