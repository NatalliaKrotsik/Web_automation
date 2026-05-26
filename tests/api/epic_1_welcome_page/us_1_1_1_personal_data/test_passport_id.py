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
            f"Response must contain LP-43 error text [{case_id}]"
        ).contains(expected_error)

@allure.story("Passport ID")
class TestPassportId(_PersonalInfoBase):
    """LP-42 — valid: digits only, 7-char min boundary, 8, 19, 20-char max boundary.
    LP-43 — invalid: capitals only, lowercase, fewer than 3 digits, empty, special chars, 6-char below min, 21-char above max."""
    
    @pytest.mark.qase("LP-42")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("passport_id", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — valid input accepted: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])
    
    @pytest.mark.qase("LP-43")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("passport_id", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — invalid input rejected: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))
