import allure
import pytest
import yaml
from assertpy import assert_that


def _load_data() -> dict:
    with open("tests/api/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()


def _params(field: str, category: str) -> list:
    return [pytest.param(c, id=c["id"]) for c in _DATA[field][category]]


pytestmark = [pytest.mark.api]


@allure.parent_suite("API Tests")
@allure.suite("Registration") 
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    pass


def _assert_valid(r, value, case_id):
    assert_that(r.status_code).described_as(
        f"Expected 201 for value={value!r} [{case_id}]"
    ).is_equal_to(201)
    assert_that(r.json()["valid"]).described_as(
        f"Response valid flag should be true [{case_id}]"
    ).is_true()


def _assert_invalid(r, value, case_id, expected_error=None):
    assert_that(r.status_code).described_as(
        f"Expected 4xx for value={value!r} [{case_id}]"
    ).is_in(400, 422)
    if expected_error:
        error_messages = [
            m["message"]
            for errors in r.json().get("details", {}).values()
            for m in errors
        ]
        assert_that(error_messages).described_as(
            f"Response must contain LP-46, LP-48 error text [{case_id}]"
        ).contains(expected_error)


@allure.story("Birth date")
class TestBirthDate(_PersonalInfoBase):
    """LP-48 — valid: standard date, leap year Feb 29 (2020, 2000), non-leap Feb 28 (1998, 2021). LP-46 — invalid: future date, more than 100 years ago, non-leap Feb 29,
    invalid day (00, 32), invalid month (00, 23), invalid year (3 digits). Note: API expects DD\\MM\\YYYY (backslash separator)."""

    @pytest.mark.qase("LP-48")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("birth_date", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Birth date — valid input accepted: {case['id']}")
        with allure.step(f"Override birth_date with {case['value']!r}"):
            valid_payload["birth_date"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    