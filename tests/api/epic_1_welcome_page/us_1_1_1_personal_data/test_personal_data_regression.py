import allure
import pytest
import yaml
from assertpy import assert_that


#  Data loading 

def _load_data() -> dict:
    with open("tests/api/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()


def _params(field: str, category: str) -> list:
    return [pytest.param(c, id=c["id"]) for c in _DATA[field][category]]


# Pytest marks (pytest-native only — Allure labels go on the base class) 

pytestmark = [pytest.mark.api, pytest.mark.regression]
# Shared base class

@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """
    Shared Allure three-level hierarchy for all personal-info test classes.
    Subclasses inherit labels without re-declaring them.
    """


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
            m["message"]
            for errors in r.json().get("details", {}).values()
            for m in errors
        ]
        assert_that(error_messages).described_as(
            f"Response must contain LP-353 error text [{case_id}]"
        ).contains(expected_error)


# First Name

@allure.story("First name")
@pytest.mark.qase("LP-353")
class TestFirstName(_PersonalInfoBase):
    """LP-353 Steps 1, 2, 15 — Polish chars, mixed register, hyphen, 30-char boundary accepted; Cyrillic and blank rejected."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("first_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — valid input accepted: {case['id']}")
        with allure.step(f"Override first_name with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("first_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — invalid input rejected: {case['id']}")
        with allure.step(f"Override first_name with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Last Name

@allure.story("Last name")
@pytest.mark.qase("LP-353")
class TestLastName(_PersonalInfoBase):
    """LP-353 Steps 3, 4, 17 — Polish chars, mixed register, hyphen, 30-char boundary accepted; Cyrillic (with exact error) and blank rejected."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("last_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — valid input accepted: {case['id']}")
        with allure.step(f"Override last_name with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("last_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — invalid input rejected: {case['id']}")
        with allure.step(f"Override last_name with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))

# Middle Name

@allure.story("Middle name")
@pytest.mark.qase("LP-353")
class TestMiddleName(_PersonalInfoBase):
    """LP-353 Steps 5, 6, 16 — Polish chars, hyphen, 30-char boundary, and null (optional) accepted; Cyrillic rejected with exact error."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("middle_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — valid input accepted: {case['id']}")
        with allure.step(f"Override middle_name with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("middle_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — invalid input rejected: {case['id']}")
        with allure.step(f"Override middle_name with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Passport ID

@allure.story("Passport ID")
@pytest.mark.qase("LP-353")
class TestPassportId(_PersonalInfoBase):
    """LP-353 Steps 7, 8, 9, 18 — capital letters + digits at max (20) and min (7) boundaries accepted; lowercase (with exact error) and blank rejected."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("passport_id", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — valid input accepted: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("passport_id", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — invalid input rejected: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Birth Date

@allure.story("Birth date")
@pytest.mark.qase("LP-353")
class TestBirthDate(_PersonalInfoBase):
    """LP-353 Steps 10, 12, 13, 14 — valid date and leap year Feb 29 accepted; wrong format, month 13, and non-leap Feb 29 rejected.
    Note: API expects DD\\MM\\YYYY (backslash). Step 11 (empty field) is UI-only, skipped pending MQA clarification."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("birth_date", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Birth date — valid input accepted: {case['id']}")
        with allure.step(f"Override birth_date with {case['value']!r}"):
            valid_payload["birth_date"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            _assert_valid(r, case["value"], case["id"])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("birth_date", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Birth date — invalid input rejected: {case['id']}")
        with allure.step(f"Override birth_date with {case['value']!r}"):
            valid_payload["birth_date"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            _assert_invalid(r, case["value"], case["id"], case.get("expected_error"))


# Happy Path

@allure.story("Happy path")
@pytest.mark.smoke
@pytest.mark.qase("LP-353")
class TestHappyPath(_PersonalInfoBase):
    """LP-353 Step 19 — all valid fields combined, system accepts and saves data."""

    @allure.title("Happy path — all valid fields submitted successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_all_valid_fields(self, api):
        hp = _DATA["happy_path"]
        with allure.step("Build LP-353 Step 19 payload"):
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