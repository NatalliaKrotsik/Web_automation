---
name: pretty-test-writer
description: >
  Use this skill whenever the user wants to write, review, fix, or extend
  automated tests in the PRetty framework. Triggers include: writing a new
  test, adding test cases, creating a Page Object, adding fixtures,
  creating YAML data files, reviewing a test for rule violations, or
  asking how to test a specific feature. Always use this skill when the
  user mentions pytest, Playwright, assertpy, Allure, Qase, or YAML test
  data in the context of this project — even if they don't say "skill"
  or "framework".
---

# PRetty Test Writer

Writes and reviews automated tests for the PRetty framework (PrettyBank),
following its strict conventions for API, UI, and DB testing.

---

## Before writing anything

1. Identify test type: **API** (`tests/api/`), **UI** (`tests/ui/`), or **DB** (`tests/db/`)
2. Identify the feature — one file per feature, one class per file
3. Identify data scenarios — these go in YAML, never inline in the test

---

## Files to create

For a new test, always create two files:

```
tests/<type>/epic_<n>_<name>/us_<n>_<n>_<name>/test_<feature>.py
tests/<type>/epic_<n>_<name>/data/<feature>.yaml
```

For a new UI test, also create or update:

```
framework/ui/pages/<feature>_page.py
```

---

## Allure Base Class Pattern (required in every test file)

Every test file must define a private `_<Suite>Base` class holding the three-level
Allure hierarchy. All test classes in the file inherit from it.

```python
@allure.parent_suite("API Tests")          # always "API Tests" or "UI Tests"
@allure.suite("Registration")              # epic name
@allure.sub_suite("US-1.1.1 Personal Info") # user story
class _PersonalInfoBase:
    """Shared Allure hierarchy for all personal-info test classes."""


@allure.story("First name")
@pytest.mark.qase("LP-36", "LP-37")
class TestFirstName(_PersonalInfoBase):
    ...

@allure.story("Last name")
@pytest.mark.qase("LP-39")
class TestLastName(_PersonalInfoBase):
    ...
```

The MRO-walking hook in `tests/conftest.py` propagates `parent_suite`, `suite`,
and `sub_suite` from the base class to every test method automatically.
**Do not repeat these on concrete test classes** — inheriting is enough.

The `_` prefix prevents pytest from collecting the base class as a test class.

---

## Test file template

```python
import allure
import pytest
from assertpy import assert_that          # API tests
from playwright.sync_api import expect    # UI tests only

from framework.api.<module> import <APIClass>   # correct imports only


pytestmark = [pytest.mark.api]   # or pytest.mark.ui


# --- Allure base class ---

@allure.parent_suite("API Tests")
@allure.suite("<Epic Name>")
@allure.sub_suite("<US-x.x.x Feature Name>")
class _<Feature>Base:
    """Shared Allure hierarchy for all <feature> test classes."""


# --- Test classes ---

@allure.story("<Story name>")
@pytest.mark.qase("<CASE-ID>")
class Test<FeatureName>(_<Feature>Base):
    """<Qase case id> — brief description of what is covered."""

    test_data_map = {
        "<fixture_arg_name>": [
            {"name": "happy_path_description",   ...},
            {"name": "failure_case_description", ...},
            {"name": "edge_case_empty_string",   ...},
        ]
    }

    @allure.title("<What is tested> — {<fixture_arg_name>}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke   # add if smoke-worthy
    def test_<specific_behavior>(self, <fixture_arg_name>, <other_fixtures>):
        with allure.step("Arrange / build payload"):
            ...
        with allure.step("Act / call API or interact with UI"):
            ...
        with allure.step("Assert <what>"):
            assert_that(...).described_as("Failure reason").is_equal_to(...)
```

---

## Parametrization — always Pattern A

Never use `@pytest.mark.parametrize` for data-driven tests.
Always define `test_data_map` on the class; `pytest_generate_tests` does the rest.

```python
test_data_map = {
    "first_name_case": [                          # key = fixture arg name in test method
        {"name": "valid_polish_chars",  "value": "Łódź", "expected_status": 201},
        {"name": "too_short_one_char",  "value": "A",    "expected_status": 400},
        {"name": "empty_string",        "value": "",     "expected_status": 400},
        {"name": "hyphen_at_start",     "value": "-Abc", "expected_status": 400},
    ]
}

def test_first_name(self, first_name_case, api):
    r = api.submit(first_name=first_name_case["value"])
    assert_that(r.status_code).described_as("Unexpected status").is_equal_to(
        first_name_case["expected_status"]
    )
```

`@allure.title` must include the fixture arg in braces so each parametrized case
gets a unique title: `"First name validation — {first_name_case}"`.

---

## YAML data file template

```yaml
# tests/<type>/epic_<n>/data/<feature>.yaml

<fixture_argument_name>:
  - name: happy_path_valid_input
    value: "ValidInput"
    expected_status: 201

  - name: failure_case_special_chars
    value: "Invalid!"
    expected_status: 400
    expected_error: "Special characters are not allowed."

  - name: edge_case_empty_string
    value: ""
    expected_status: 400
    expected_error: "Field is required."

  - name: edge_case_max_boundary
    value: "Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"   # 30 chars
    expected_status: 201
```

Rules:
- Key name = fixture argument name in `test_data_map`
- Every entry must have a `name` field — lowercase with underscores
- Always include: happy path, failure cases, edge cases (empty, max/min boundary, special chars)
- One scenario per entry — never duplicate, add a new entry instead
- No unnecessary nesting; consistent field names across all YAML files

---

## Fixture rules

```python
@pytest.fixture(scope="session")       # always explicit scope
def auth_tokens(load_environment) -> dict:    # always depend on load_environment
    """Retrieves authentication tokens."""
    auth_api = AuthAPI()
    tokens = auth_api.authorization(
        email=EnvManager.get("USER_EMAIL_DEV"),
        password=EnvManager.get("USER_PASSWORD_DEV"),
    )
    return tokens.json()
```

- `scope="session"` for auth and shared resources that don't change between tests
- `scope="function"` for anything that mutates state
- Every auth fixture must declare `load_environment` as a dependency
- Never use `os.getenv()` — always `EnvManager.get()`
- Never hardcode URLs — always `EnvManager.get_config()`
- No assertions inside fixtures — raise `RuntimeError` with a clear message instead
- Fixtures that create resources must clean up via `yield`

---

## Page Object rules (UI only)

```python
from playwright.sync_api import Page

from framework.env_manager import EnvManager
from framework.ui.core.base_page import BasePage


class SomePage(BasePage):
    """Handles interactions on the Some page."""

    def __init__(self, page: Page):
        super().__init__(page, EnvManager.get_config().base_url + "/some-path")
        self._submit_button = page.get_by_role("button", name="Submit")

    def click_submit_button(self) -> None:
        with allure.step("Click submit button"):
            self._submit_button.click()
```

- Inherits from `BasePage`; element classes inherit from `BaseElement`
- Locators live here only — never in test files
- Method names describe user actions: `click_login_button()` not `click_button()`
- URLs come from `EnvManager.get_config()` — never hardcoded
- Use the framework `page` fixture (from `tests/conftest.py`) — never import raw Playwright `Page` in tests

---

## Assertions reference

| Context  | Library        | Example |
|----------|----------------|---------|
| API      | assertpy       | `assert_that(r.status_code).described_as("Should be 201").is_equal_to(201)` |
| UI       | Playwright expect | `expect(page.locator(...)).to_be_visible()` |
| Security | assertpy       | `assert_that(r.status_code).described_as("Should be 401 or 403").is_in(401, 403)` |

- Never assert just `True` / `False`
- Never use conditional assertions
- Always include `.described_as()` on assertpy assertions
- Security tests: only `401` or `403` — never `404`

---

## Allure severity guide

| Level    | When to use |
|----------|-------------|
| `BLOCKER`  | Login, payment, core registration — app unusable without it |
| `CRITICAL` | Core business features |
| `NORMAL`   | Standard features |
| `MINOR`    | Cosmetic, edge cases, low-impact |

Never mark everything `BLOCKER` or `CRITICAL`.

---

## Markers

All markers must be registered in `pyproject.toml` and `pytest.ini`.

- `@pytest.mark.api` — all API tests
- `@pytest.mark.ui` — all UI tests
- `@pytest.mark.smoke` — critical path, fast
- `@pytest.mark.regression` — full suite
- `@pytest.mark.qase(id)` — links to Qase test case; required where a case exists

---

## Environment

- Secrets live in `env/.env.<env>` — loaded automatically by `load_environment` fixture
- `env/.env.example` is the template for new team members — keep it up to date
- Never commit real credentials
- Never use `os.getenv()` directly

---

## Review mode

When asked to review an existing test, check every section of the checklist in
CLAUDE.md and output violations grouped by category:

```
[Parametrize] test_birthday uses @pytest.mark.parametrize — must use test_data_map instead
[Fixtures]    admin_auth_tokens missing load_environment dependency
[Allure]      TestAddress has no _AddressBase — parent_suite/suite/sub_suite not set
```

If no violations, say so explicitly.
