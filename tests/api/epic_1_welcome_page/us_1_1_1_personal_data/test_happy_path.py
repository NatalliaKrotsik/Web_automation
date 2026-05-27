import allure
import pytest
import yaml
from assertpy import assert_that


def _load_data() -> dict:
    with open("tests/api/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()

pytestmark = [pytest.mark.api, pytest.mark.smoke]


@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    pass


@allure.story("Happy path")
@pytest.mark.qase("LP-75")
class TestHappyPath(_PersonalInfoBase):
    """LP-75 — all valid fields submitted together, system accepts and returns valid=true."""
    @allure.title("Happy path — all valid fields submitted successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_all_valid_fields(self, api):
        hp = _DATA["happy_path"]
        with allure.step("Build happy path payload"):
            payload = {
                "first_name":  hp["first_name"],
                "middle_name": hp["middle_name"],
                "last_name":   hp["last_name"],
                "passport_id": hp["passport_id"],
                "birth_date":  hp["birth_date"],
            }
        with allure.step("Submit and assert 201 with valid=true"):
            r = api.submit_personal_info(**payload)
            assert_that(r.status_code).described_as(
                "Happy path should return 201"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                "Happy path response valid flag should be true"
            ).is_true()
