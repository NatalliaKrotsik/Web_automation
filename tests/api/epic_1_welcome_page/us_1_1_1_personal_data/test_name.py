import allure
import pytest
import yaml
from assertpy import assert_that


# Data loading

def _load_data() -> dict:
    with open("tests/api/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()


def _params(field: str, category: str) -> list:
    return [pytest.param(c, id=c["id"]) for c in _DATA[field][category]]


# Pytest marks

pytestmark = [pytest.mark.api]


# Shared base class

@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure three-level hierarchy for all name test classes."""


# Helpers

def _assert_valid(r, value, case_id):
    assert_that(r.status_code).described_as(
        f"Expected 201 for value={value!r} [{case_id}]"
    ).is_equal_to(201)
    assert_that(r.json()["valid"]).described_as(
        f"Response valid flag should be true [{case_id}]"
    ).is_true()


def _assert_invalid(r, value, case_id, expected_error=None):
    assert_that(r.status_code).described_as(
        f"Expected 422 for value={value!r} [{case_id}]"
    ).is_equal_to(422)
    if expected_error:
        error_messages = [
            e["message"]
            for errors in r.json().get("details", {}).values()
            for e in errors
        ]
        assert_that(error_messages).described_as(
            f"Response must contain error text [{case_id}]"
        ).contains(expected_error)


# First Name

@allure.story("First name")
@pytest.mark.qase("LP-36", "LP-37")
class TestFirstName(_PersonalInfoBase):
    """
    LP-36 — valid: Polish chars, mixed register, hyphen, apostrophe,
             2-char min, 30-char max, trailing spaces trimmed,
             internal spaces collapsed.
    LP-37 — invalid: special chars, 1-char below min, 31-char above max,
             spaces only, hyphen at start/end.
    """

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("first_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — valid input accepted: {case['id']}")
        with allure.step(f"Override firstName with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("first_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — invalid input rejected: {case['id']}")
        with allure.step(f"Override firstName with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 422 rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Last Name

@allure.story("Last name")
@pytest.mark.qase("LP-39", "LP-41")
class TestLastName(_PersonalInfoBase):
    """
    LP-39 — valid: mixed register, hyphen, apostrophe, 2-char min,
             30-char max, Polish chars, lowercase stored as capitalised,
             trailing spaces trimmed, internal spaces collapsed.
    LP-41 — invalid: special chars, 1-char below min, 31-char above max,
             spaces only, hyphen at start/end.
    """

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("last_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — valid input accepted: {case['id']}")
        with allure.step(f"Override lastName with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("last_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — invalid input rejected: {case['id']}")
        with allure.step(f"Override lastName with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 422 rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Middle Name

@allure.story("Middle name")
@pytest.mark.qase("LP-329", "LP-330")
class TestMiddleName(_PersonalInfoBase):
    """
    LP-329 — valid: Latin letters, Polish chars, empty/null (optional),
              2-char min, 3-char, 29-char, 30-char boundaries,
              mixed register, hyphen in middle accepted.
    LP-330 — invalid: 1-char below min, 31-char above max,
              Russian/Belarusian letters, special char pairs,
              hyphen at start/end, digits.
    """

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("middle_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — valid input accepted: {case['id']}")
        with allure.step(f"Override middleName with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("middle_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — invalid input rejected: {case['id']}")
        with allure.step(f"Override middleName with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 422 rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Capitalisation (LP-331 step 3)
@allure.story("Name capitalisation")
@pytest.mark.qase("LP-331")
class TestNameFormatting(_PersonalInfoBase):
    """
    LP-331 step 3 — system stores names capitalised regardless of input register.
    e.g. lódź-nova -> Lódź-Nova, środa-buLgA -> Środa-Bulga
    Skipped: 201 returns only valid=true — capitalisation storage
    needs DB assertion, pending db fixture setup.
    """

    @pytest.mark.skip(
        reason="201 returns only valid=true — capitalisation storage needs DB assertion, pending db fixture setup"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("name_formatting", "valid"))
    def test_capitalisation_stored_correctly(self, api, valid_payload, case):
        allure.dynamic.title(f"Capitalisation — {case['id']}")
        with allure.step(f"Override names with mixed-case input: {case['id']}"):
            valid_payload["first_name"] = case["first_name"]
            valid_payload["middle_name"] = case["middle_name"]
            valid_payload["last_name"] = case["last_name"]
        with allure.step("Submit and assert 201"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for capitalisation case [{case['id']}]"
            ).is_equal_to(201)
        with allure.step(f"Assert stored format matches expected: {case['expected']}"):
            body = r.json()
            assert_that(body.get("firstName")).described_as(
                f"firstName should be stored as {case['expected']['first_name']!r}"
            ).is_equal_to(case["expected"]["first_name"])
            assert_that(body.get("lastName")).described_as(
                f"lastName should be stored as {case['expected']['last_name']!r}"
            ).is_equal_to(case["expected"]["last_name"])
            assert_that(body.get("middleName")).described_as(
                f"middleName should be stored as {case['expected']['middle_name']!r}"
            ).is_equal_to(case["expected"]["middle_name"])