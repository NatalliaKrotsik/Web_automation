import allure
import pytest
import yaml
from assertpy import assert_that

from framework.api.personal_data_api import PersonalDataAPI


def _load_data() -> dict:
    with open("tests/api/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()
_BASELINE = _DATA["valid_baseline"]


def _params(field: str, category: str) -> list:
    return [pytest.param(c, id=c["id"]) for c in _DATA[field][category]]


@pytest.fixture(scope="function")
def api() -> PersonalDataAPI:
    return PersonalDataAPI()


@pytest.fixture(scope="function")
def valid_payload() -> dict:
    """Baseline valid payload per LP-353 pre-conditions."""
    return {
        "first_name":  _BASELINE["first_name"],
        "middle_name": _BASELINE["middle_name"],
        "last_name":   _BASELINE["last_name"],
        "passport_id": _BASELINE["passport_id"],
        "birth_date":  _BASELINE["birth_date"],
    }


# ── First Name 

@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("First name")
class TestFirstNameValid:
    """LP-353 Step 1 — first name accepts Polish characters, mixed register, hyphen, 30-char boundary."""

    @allure.title("First name — valid input accepted")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("first_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — valid input accepted: {case['id']}")
        with allure.step(f"Override first_name with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for first_name={case['value']!r} [{case['id']}]"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                f"Response valid flag should be true [{case['id']}]"
            ).is_true()


@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("First name")
class TestFirstNameInvalid:
    """LP-353 Steps 2, 15 — Cyrillic and blank first name are rejected."""

    @allure.title("First name — invalid input rejected")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("first_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"First name — invalid input rejected: {case['id']}")
        with allure.step(f"Override first_name with {case['value']!r}"):
            valid_payload["first_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 4xx for invalid first_name={case['value']!r} [{case['id']}]"
            ).is_in(400, 422)
            assert_that(r.json().get("valid")).described_as(
                f"valid flag must not be true for invalid input [{case['id']}]"
            ).is_not_equal_to(True)
        if case.get("expected_error"):
            with allure.step(f"Assert error message: {case['expected_error']!r}"):
                error_messages = [
                    m["message"]
                    for errors in r.json().get("details", {}).values()
                    for m in errors
                ]
                assert_that(error_messages).described_as(
                    f"Response must contain LP-353 error text [{case['id']}]"
                ).contains(case["expected_error"])


# ── Last Name 

@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Last name")
class TestLastNameValid:
    """LP-353 Step 3 — last name accepts Polish characters, mixed register, hyphen, 30-char boundary."""

    @allure.title("Last name — valid input accepted")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("last_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — valid input accepted: {case['id']}")
        with allure.step(f"Override last_name with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for last_name={case['value']!r} [{case['id']}]"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                f"Response valid flag should be true [{case['id']}]"
            ).is_true()


@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Last name")
class TestLastNameInvalid:
    """LP-353 Steps 4, 17 — Cyrillic and blank last name are rejected; Cyrillic returns exact LP-353 error message."""

    @allure.title("Last name — invalid input rejected")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("last_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Last name — invalid input rejected: {case['id']}")
        with allure.step(f"Override last_name with {case['value']!r}"):
            valid_payload["last_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 4xx for invalid last_name={case['value']!r} [{case['id']}]"
            ).is_in(400, 422)
            assert_that(r.json().get("valid")).described_as(
                f"valid flag must not be true for invalid input [{case['id']}]"
            ).is_not_equal_to(True)
        if case.get("expected_error"):
            with allure.step(f"Assert error message: {case['expected_error']!r}"):
                error_messages = [
                    m["message"]
                    for errors in r.json().get("details", {}).values()
                    for m in errors
                ]
                assert_that(error_messages).described_as(
                    f"Response must contain LP-353 error text [{case['id']}]"
                ).contains(case["expected_error"])


# ── Middle Name

@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Middle name")
class TestMiddleNameValid:
    """LP-353 Steps 5, 16 — middle name accepts Polish characters, mixed register, hyphen, 30-char boundary, and null (field is optional)."""

    @allure.title("Middle name — valid input accepted")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("middle_name", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — valid input accepted: {case['id']}")
        with allure.step(f"Override middle_name with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for middle_name={case['value']!r} [{case['id']}]"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                f"Response valid flag should be true [{case['id']}]"
            ).is_true()


@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Middle name")
class TestMiddleNameInvalid:
    """LP-353 Step 6 — Cyrillic middle name is rejected with exact LP-353 error message."""

    @allure.title("Middle name — invalid input rejected")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("middle_name", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Middle name — invalid input rejected: {case['id']}")
        with allure.step(f"Override middle_name with {case['value']!r}"):
            valid_payload["middle_name"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 4xx for invalid middle_name={case['value']!r} [{case['id']}]"
            ).is_in(400, 422)
            assert_that(r.json().get("valid")).described_as(
                f"valid flag must not be true for invalid input [{case['id']}]"
            ).is_not_equal_to(True)
        if case.get("expected_error"):
            with allure.step(f"Assert error message: {case['expected_error']!r}"):
                error_messages = [
                    m["message"]
                    for errors in r.json().get("details", {}).values()
                    for m in errors
                ]
                assert_that(error_messages).described_as(
                    f"Response must contain LP-353 error text [{case['id']}]"
                ).contains(case["expected_error"])


# ── Passport ID

@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Passport ID")
class TestPassportIdValid:
    """LP-353 Steps 7, 9 — passport ID accepts capital Latin letters + digits at max (20) and min (7) boundaries."""

    @allure.title("Passport ID — valid input accepted")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("passport_id", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — valid input accepted: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for passport_id={case['value']!r} [{case['id']}]"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                f"Response valid flag should be true [{case['id']}]"
            ).is_true()


@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Passport ID")
class TestPassportIdInvalid:
    """LP-353 Steps 8, 18 — lowercase and blank passport ID are rejected."""

    @allure.title("Passport ID — invalid input rejected")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("passport_id", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Passport ID — invalid input rejected: {case['id']}")
        with allure.step(f"Override passport_id with {case['value']!r}"):
            valid_payload["passport_id"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 4xx for invalid passport_id={case['value']!r} [{case['id']}]"
            ).is_in(400, 422)
            assert_that(r.json().get("valid")).described_as(
                f"valid flag must not be true for invalid input [{case['id']}]"
            ).is_not_equal_to(True)
        if case.get("expected_error"):
            with allure.step(f"Assert error message: {case['expected_error']!r}"):
                error_messages = [
                    m["message"]
                    for errors in r.json().get("details", {}).values()
                    for m in errors
                ]
                assert_that(error_messages).described_as(
                    f"Response must contain LP-353 error text [{case['id']}]"
                ).contains(case["expected_error"])
# ── Birth Date

@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Birth date")
class TestBirthDateValid:
    """LP-353 Steps 10, 14 — valid date and leap year Feb 29 are accepted.
    Note: API expects DD\\MM\\YYYY (backslash). Step 11 (empty field) is UI-only, skipped pending MQA clarification."""

    @allure.title("Birth date — valid input accepted")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", _params("birth_date", "valid"))
    def test_valid_input(self, api, valid_payload, case):
        allure.dynamic.title(f"Birth date — valid input accepted: {case['id']}")
        with allure.step(f"Override birth_date with {case['value']!r}"):
            valid_payload["birth_date"] = case["value"]
        with allure.step("Submit personal info — assert 201 and valid=true"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 201 for birth_date={case['value']!r} [{case['id']}]"
            ).is_equal_to(201)
            assert_that(r.json()["valid"]).described_as(
                f"Response valid flag should be true [{case['id']}]"
            ).is_true()


@pytest.mark.api
@pytest.mark.regression
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Birth date")
class TestBirthDateInvalid:
    """LP-353 Steps 12, 13, 14 — wrong format, month 13, and non-leap Feb 29 are rejected."""

    @allure.title("Birth date — invalid input rejected")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", _params("birth_date", "invalid"))
    def test_invalid_input_rejected(self, api, valid_payload, case):
        allure.dynamic.title(f"Birth date — invalid input rejected: {case['id']}")
        with allure.step(f"Override birth_date with {case['value']!r}"):
            valid_payload["birth_date"] = case["value"]
        with allure.step("Submit personal info — assert 4xx rejection"):
            r = api.submit_personal_info(**valid_payload)
            assert_that(r.status_code).described_as(
                f"Expected 4xx for invalid birth_date={case['value']!r} [{case['id']}]"
            ).is_in(400, 422)
            assert_that(r.json().get("valid")).described_as(
                f"valid flag must not be true for invalid input [{case['id']}]"
            ).is_not_equal_to(True)
        if case.get("expected_error"):
            with allure.step(f"Assert error message: {case['expected_error']!r}"):
                error_messages = [
                    m["message"]
                    for errors in r.json().get("details", {}).values()
                    for m in errors
                ]
                assert_that(error_messages).described_as(
                    f"Response must contain LP-353 error text [{case['id']}]"
                ).contains(case["expected_error"])


# ── Happy Path

@pytest.mark.api
@pytest.mark.smoke
@allure.suite("API Tests - Registration")
@allure.feature("US-1.1.1 Personal Info")
@allure.story("Happy path")
class TestHappyPath:
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