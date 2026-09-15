# CLAUDE.md

Guidance for Claude Code when working in the web test automation framework.

## Project Overview

UI + API + DB test automation framework for **web** — an internal banking web application.
Stack: Python 3.11+, pytest, Playwright, Requests, SQLAlchemy, Allure, Qase.

---

## Commands

```bash
# Install dependencies
poetry install
playwright install chromium

# Activate pre-commit hooks (required once after clone)
pre-commit install

# Run all tests
poetry run pytest tests/ --env=dev

# Run a single test file
poetry run pytest tests/api/epic_1_welcome_page/us_1_1_3_input_address_info/test_address_info.py --env=dev

# Run by marker
poetry run pytest -m api --env=dev
poetry run pytest -m ui --env=dev

# Parallel run (matches CI)
poetry run pytest -n 4 --env=dev

# View Allure report locally
allure serve allure-results

# Lint and format
poetry run ruff check .
poetry run black .
```

Available `--env` values: `dev`, `test`, `prod`. Always use `--env=dev` — the `test` environment is currently not operational.

---

## Project Structure

```
project/
├── framework/
│   ├── env_manager.py              # EnvManager singleton
│   ├── api/                        # HttpClient + API classes
│   ├── ui/
│   │   └── pages/                  # Page Object classes
│   └── data_base/
│       └── db_client.py
├── tests/
│   ├── conftest.py                 # env loading, browser/page fixtures, MRO Allure hook
│   ├── api/
│   │   ├── conftest.py             # auth_tokens, admin_auth_tokens
│   │   └── epic_<n>_<name>/
│   │       ├── conftest.py         # epic-level fixtures
│   │       ├── data/               # YAML test data files
│   │       └── us_<n>_<n>_<name>/ # one folder per user story
│   ├── ui/
│   │   ├── conftest.py
│   │   └── epic_<n>_<name>/
│   │       └── us_<n>_<n>_<name>/
│   └── db/
├── configs/                        # Per-environment YAML config files
│   ├── dev.yaml
│   ├── test.yaml
│   └── prod.yaml
├── env/                            # Secret env files — never committed
│   ├── .env.dev
│   ├── .env.test
│   └── .env.example                # Template for required variables
├── pyproject.toml
├── pytest.ini
└── .pre-commit-config.yaml
```

---

## Architecture

### Configuration (`framework/env_manager.py`)

`EnvManager` is a session-scoped singleton. Call `EnvManager.load(env)` once (done automatically by the `load_environment` fixture in `tests/conftest.py`).

- Loads URLs and browser settings from `configs/<env>.yaml`
- Loads secrets from `env/.env.<env>` via `python-dotenv`

```python
EnvManager.get_config()        # → EnvConfig (base_url, ui, api)
EnvManager.get("VAR_NAME")     # → str from env file; raises RuntimeError if missing
```

Never use `os.getenv()` directly. Never hardcode URLs or credentials anywhere.

Required variables in `env/.env.<env>`:
- `USER_EMAIL_DEV`, `USER_PASSWORD_DEV` — regular user credentials
- `ADMIN_USER_EMAIL`, `ADMIN_USER_PASSWORD` — admin credentials
- `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME` — database connection

The `env/.env.example` file exists as a template for new team members — keep it up to date.

### API Layer (`framework/api/`)

`HttpClient` (base class) handles URL building, `requests.Session`, and automatic Allure attachment of request/response. All API classes inherit from it:

```
HttpClient
├── AuthAPI           → api/auth/sign-in, sign-out, session/ping
├── PersonalDataAPI
├── AddressAPI        → api/registration/address
└── ExchangeRatesAPI
```

Never instantiate API classes directly inside tests — use fixtures.

### UI Layer (`framework/ui/pages/`)

Page Object Model:
- `BasePage` — wraps Playwright `Page`: `open()`, navigation helpers, clipboard utility
- `BaseElement` — wraps a locator with common interactions
- All page classes inherit from `BasePage`; all element classes inherit from `BaseElement`

### Database Layer (`framework/data_base/db_client.py`)

`DbClient` uses SQLAlchemy Core against PostgreSQL `public.user_user`. Provides `user_exists()`, `get_user_data()`, and `wait_until_user_created()` (polls up to 30s).

---

## Structure & Naming Rules

- Every test must be inside a class — never a standalone function
- One test file covers one feature or one page only
- One test verifies one behavior only
- Test files: `test_<feature_name>.py`
- Test classes: `Test<FeatureName>`
- API tests → `tests/api/`, UI tests → `tests/ui/`, DB tests → `tests/db/`
- Test names must describe what is tested and what is expected — never `test_api`, `test_check`, `test_flow`
- Fixture names must be nouns — `auth_tokens` not `get_tokens`
- YAML `name` field values must be lowercase with underscores

---

## Parametrization & Test Data

**Always use Pattern A — `test_data_map` + `pytest_generate_tests`.** Never use `@pytest.mark.parametrize` for data-driven tests.

```python
class TestFirstName(_SuiteBase):
    test_data_map = {
        "first_name_case": [
            {"name": "valid_polish_chars", "value": "Łódź", "expected_status": 201},
            {"name": "too_short_one_char", "value": "A",    "expected_status": 400},
            {"name": "empty_string",       "value": "",     "expected_status": 400},
        ]
    }

    @allure.title("First name validation — {first_name_case}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_first_name(self, first_name_case, api):
        with allure.step(f"Submit value: {first_name_case['value']}"):
            r = api.submit(first_name=first_name_case["value"])
        with allure.step("Assert status code"):
            assert_that(r.status_code).described_as("Unexpected status").is_equal_to(first_name_case["expected_status"])
```

`pytest_generate_tests` in `tests/conftest.py` reads `test_data_map`, parametrizes matching fixture names automatically, and uses the `"name"` key for readable test IDs.

Test data files live in `tests/<type>/epic_<n>_<name>/data/`. Two formats are allowed — choose one per file and stay consistent within it:

**Option A — YAML** (`<feature>.yaml`):
```yaml
- name: valid_polish_chars
  value: "Łódź"
  expected_status: 201

- name: too_short_one_char
  value: "A"
  expected_status: 400
```

**Option B — Python** (`<feature>_data.py`):
```python
FIRST_NAME_CASES = [
    {"name": "valid_polish_chars", "value": "Łódź", "expected_status": 201},
    {"name": "too_short_one_char", "value": "A",    "expected_status": 400},
]
```
Import the list directly into `test_data_map` inside the test class:
```python
from tests.api.epic_1_welcome_page.data.first_name_data import FIRST_NAME_CASES

class TestFirstName(_SuiteBase):
    test_data_map = {"first_name_case": FIRST_NAME_CASES}
```

Rules that apply to **both** formats:
- Every entry must have a `name` field (lowercase with underscores)
- Always include happy path, failure cases, and edge cases
- Never duplicate entries — add a new entry instead
- Never put raw data inline inside the test method itself

---

## Allure Labels — Base Class + MRO Pattern

**Always define a private `_<Suite>Base` class per test file to hold the three-level Allure hierarchy. All test classes in that file inherit from it.**

```python
@allure.parent_suite("API Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.1 Personal Info")
class _PersonalInfoBase:
    """Shared Allure hierarchy for all personal-info test classes."""


@allure.story("First name")
@pytest.mark.qase("LP-36", "LP-37")
class TestFirstName(_PersonalInfoBase):
    ...

@allure.story("Last name")
@pytest.mark.qase("LP-39", "LP-41")
class TestLastName(_PersonalInfoBase):
    ...
```

The MRO-walking hook in `tests/conftest.py` (`pytest_runtest_setup`) automatically propagates `@allure_label` markers from base classes to every test method. You do **not** need to repeat `@allure.parent_suite`, `@allure.suite`, or `@allure.sub_suite` on each class — inheriting from `_<Suite>Base` is enough.

The base class name starts with `_` (underscore) so pytest does not collect it as a test class.

---

## Fixtures

- Every fixture must have an explicit scope — never rely on the default `function` scope
- Use `scope="session"` for authentication and shared resources
- Use `scope="function"` for anything that mutates state
- Never put assertions inside fixtures — raise `RuntimeError` with a clear message instead
- Always use `EnvManager.get()` for secrets, `EnvManager.get_config()` for URLs
- Fixtures that create resources must clean them up using `yield`
- Every auth fixture must declare `load_environment` as a dependency — including `admin_auth_tokens`

```python
# CORRECT ✅
@pytest.fixture(scope="session")
def admin_auth_tokens(load_environment) -> dict:
    auth_api = AuthAPI()
    tokens = auth_api.authorization(
        email=EnvManager.get("ADMIN_USER_EMAIL"),
        password=EnvManager.get("ADMIN_USER_PASSWORD")
    )
    return tokens.json()
```

---

## Page Object Rules (UI Tests Only)

- All locators live in `framework/ui/pages/` — never in test files
- All page interactions live in Page Object methods — never in test files
- Every page object inherits from `BasePage`; every element class inherits from `BaseElement`
- Always use the framework `page` fixture from `tests/conftest.py` — never import raw Playwright `Page` in tests
- URLs come from `EnvManager.get_config()` — never hardcoded
- Method names describe user actions: `click_login_button()` not `click_button()`

---

## Assertions

- Use `assertpy` for API tests, Playwright `expect()` for UI tests — never mixed
- Always add `.described_as("reason")` to assertpy assertions
- Never use conditional assertions
- Never assert just `True` or `False` — assert the specific value
- Security tests: only accept `401` or `403` — never `404`
- Never assert multiple unrelated things in one test

---

## Waiting (UI Tests Only)

- Never use `page.wait_for_timeout()` — use Playwright's built-in smart waiting
- Always use `expect()` for visibility, enabled state, and text checks
- If a wait is unavoidable, keep it minimal and add a comment explaining why

---

## Allure Reporting

- `@allure.parent_suite` / `@allure.suite` / `@allure.sub_suite` — on the `_Base` class
- `@allure.story` — on each concrete test class
- `@allure.title` — on every test method; include the param name for parametrized tests: `"First name — {first_name_case}"`
- `@allure.severity` — on every test method; reflect real business impact:
  - `BLOCKER` — login, payment, core registration
  - `CRITICAL` — core features
  - `NORMAL` — standard features
  - `MINOR` — cosmetic or edge cases
- Every meaningful action must be wrapped in `with allure.step()`
- Never mark everything `BLOCKER` or `CRITICAL`

---

## Markers

- `@pytest.mark.api` — all API tests
- `@pytest.mark.ui` — all UI tests
- `@pytest.mark.smoke` — critical path, fast subset
- `@pytest.mark.regression` — full suite
- `@pytest.mark.qase(id)` — links to Qase test case; required where a case exists
- Never use undefined markers — all markers must be registered in `pyproject.toml` and `pytest.ini`

---

## Test Independence

- Every test must run alone, in any order, and still pass
- Tests must never depend on another test having run first
- Never log out inside a flow test — logout must be its own separate test
- Never share mutable state between tests

---

## Code Quality

- Never import from the wrong module — verify imports before using them
- Never leave dead code — unused fixtures, imports, or variables must be removed
- Always run pre-commit hooks before pushing (`black`, `ruff`, `pre-commit` configured)
- Every new page object, API client, or utility must have a docstring

---

## CI/CD

GitLab CI (`.gitlab-ci.yml`) runs `ui_tests` and `api_tests` in parallel with 4 workers, merges Allure results, and deploys to GitLab Pages. Allure history is preserved across pipelines via artifact download from `main`.

---

## Quick Reference Checklist

**Structure**
- [ ] Test is inside a class
- [ ] One test = one behavior
- [ ] File name starts with `test_` and matches feature name

**Naming**
- [ ] Test name describes what is tested and what is expected
- [ ] Every YAML data entry has a meaningful `name` field
- [ ] `name` values are lowercase with underscores

**Independence**
- [ ] Test does not depend on another test
- [ ] No logout inside flow tests
- [ ] No hard waits (`wait_for_timeout`)

**Test Data**
- [ ] Test data lives in `tests/.../epic_.../data/` (YAML or Python file)
- [ ] YAML file named after the test file (`<feature>.yaml`) OR Python file named `<feature>_data.py`
- [ ] Only one format used per feature — not mixed
- [ ] Every entry has a `name` field (lowercase with underscores)
- [ ] Happy path, failure cases, and edge cases all covered

**Parametrize**
- [ ] `test_data_map` used — never `@pytest.mark.parametrize` for data-driven tests
- [ ] Data loaded via `pytest_generate_tests` automatically
- [ ] No raw data inside test file

**Fixtures**
- [ ] All fixtures have explicit scope
- [ ] No assertions inside fixtures
- [ ] `EnvManager.get()` used instead of `os.getenv()`
- [ ] Fixture names are nouns
- [ ] Auth fixtures declare `load_environment` dependency

**Allure Base Class**
- [ ] `_<Suite>Base` class defined with `@allure.parent_suite`, `@allure.suite`, `@allure.sub_suite`
- [ ] All test classes in the file inherit from `_<Suite>Base`
- [ ] `@allure.story` on each concrete test class
- [ ] `@allure.title` includes param name for parametrized tests
- [ ] `@allure.severity` reflects real business impact
- [ ] Every action wrapped in `allure.step`

**Page Objects (UI only)**
- [ ] No locators inside tests
- [ ] No hardcoded URLs
- [ ] Framework `page` fixture used, not raw Playwright `Page`
- [ ] Page object inherits from `BasePage`

**Assertions**
- [ ] No conditional assertions
- [ ] `assertpy` for API, `expect` for UI
- [ ] `.described_as()` added to every assertpy assertion
- [ ] Security tests only accept `401` or `403`

**Markers**
- [ ] Correct `@pytest.mark` applied (`api`, `ui`, `smoke`, `regression`)
- [ ] `@pytest.mark.qase` linked where required
- [ ] No undefined markers used

**Environment**
- [ ] No hardcoded URLs or credentials
- [ ] `EnvManager` used everywhere
- [ ] `env/.env.example` kept up to date

**Code Quality**
- [ ] No unused imports or dead code
- [ ] Pre-commit hooks passed
- [ ] Newline at end of file
