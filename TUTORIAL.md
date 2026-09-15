# Beginner's Tutorial — Web Test Automation Framework

Welcome! This guide will take you from zero to writing and running your first API and UI tests
in the web automation framework. Read every section in order — each one builds on the previous.

---

## Table of Contents

1. [What is this framework?](#1-what-is-this-framework)
2. [Prerequisites](#2-prerequisites)
3. [Project Setup](#3-project-setup)
4. [Project Structure](#4-project-structure)
5. [Key Concepts](#5-key-concepts)
6. [Writing Your First API Test](#6-writing-your-first-api-test)
7. [Writing Your First UI Test](#7-writing-your-first-ui-test)
8. [Test Data](#8-test-data)
9. [Running Tests](#9-running-tests)
10. [Viewing the Allure Report](#10-viewing-the-allure-report)
11. [Common Mistakes to Avoid](#11-common-mistakes-to-avoid)

---

## 1. What is this framework?

This is a **Python test automation framework** for web — an internal banking web application.
It lets you write three types of automated tests:

| Type | What it tests | Tool used |
|------|--------------|-----------|
| **API** | Backend endpoints (HTTP requests/responses) | `requests` + `assertpy` |
| **UI** | Browser interactions (clicks, forms, navigation) | `Playwright` |
| **DB** | Database state after operations | `SQLAlchemy` |

Everything is glued together by **pytest** with **Allure** for reports and **Qase** for test management.

---

## 2. Prerequisites

Before you start, make sure you have the following installed:

```bash
# Check Python version — must be 3.11 or higher
python3 --version

# Check Poetry (dependency manager)
poetry --version

# If Poetry is not installed:
pip3 install poetry
```

You also need:
- Access to the GitLab repository
- The secret `.env` files (ask your team lead — they are never committed to git)

---

## 3. Project Setup

Follow these steps once after cloning the repo:

```bash
# Step 1 — Install all Python dependencies
poetry install

# Step 2 — Install the Chromium browser for Playwright
poetry run playwright install chromium

# Step 3 — Install pre-commit hooks (runs black + ruff before every git commit)
pre-commit install

# Step 4 — Create your env folder and secrets file
mkdir -p env
cp env/.env.example env/.env.dev
# Now open env/.env.dev and fill in the real values (ask your team lead)
```

Your `env/.env.dev` file should look like this (fill in real values):

```
USER_EMAIL_DEV=your_user@example.com
USER_PASSWORD_DEV=YourPassword123!
ADMIN_USER_EMAIL=admin@example.com
ADMIN_USER_PASSWORD=AdminPassword123!
DB_USER=db_user
DB_PASS=db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
```

> **Important:** The `env/` folder is in `.gitignore`. Never commit secret files.

---

## 4. Project Structure

```
web-autotests/
│
├── framework/                  ← Reusable code — do NOT put tests here
│   ├── env_manager.py          ← Reads config + secrets
│   ├── api/
│   │   ├── core/http_client.py ← Base HTTP client (all API classes inherit this)
│   │   ├── auth_api.py         ← Login / logout endpoints
│   │   ├── personal_data_api.py
│   │   └── exchange_rates_api.py
│   ├── ui/
│   │   ├── core/base_page.py   ← Base class for all page objects
│   │   ├── core/base_element.py
│   │   └── pages/              ← One file per page of the app
│   │       ├── home_page.py
│   │       ├── sign_up/personal_info_page.py
│   │       └── log_into_my_profile.py
│   └── data_base/
│       └── db_client.py
│
├── tests/                      ← All test files live here
│   ├── conftest.py             ← Session-level fixtures (browser, page, env loading)
│   ├── api/
│   │   ├── conftest.py         ← auth_tokens fixture
│   │   └── epic_1_welcome_page/
│   │       ├── conftest.py     ← Epic-level fixtures (e.g. exchange_rates_api)
│   │       ├── data/           ← Test data files (.yaml or .py)
│   │       └── us_1_15_exchange_rates/
│   │           └── test_exchange_rates.py
│   └── ui/
│       └── epic_1_welcome_page/
│           └── us_1_2_log_into_my_profile/
│               └── test_log_into_my_profile.py
│
├── configs/
│   ├── dev.yaml                ← URLs and browser settings for dev environment
│   ├── test.yaml
│   └── prod.yaml
│
├── env/                        ← Secret files — NEVER commit these
│   ├── .env.dev
│   └── .env.example            ← Template — keep this up to date
│
├── pyproject.toml              ← Dependencies and tool configuration
└── pytest.ini                  ← pytest settings
```

### The golden rule of structure

> **`framework/`** = tools you can reuse  
> **`tests/`** = the actual test scenarios

Never put test logic inside `framework/` and never put page locators or HTTP calls directly inside test files.

---

## 5. Key Concepts

### 5.1 EnvManager — configuration and secrets

`EnvManager` is the single source of truth for all URLs and credentials.
It loads two things when tests start:

1. **`configs/dev.yaml`** — non-secret settings (base URL, browser type, timeouts)
2. **`env/.env.dev`** — secret credentials (emails, passwords, DB connection)

```python
from framework.env_manager import EnvManager

# Get the base URL from configs/dev.yaml
config = EnvManager.get_config()
print(config.base_url)       # https://dev.example.com
print(config.api.base_url)   # https://api-dev.example.com

# Get a secret from env/.env.dev
email = EnvManager.get("USER_EMAIL_DEV")
```

> **Rule:** Never use `os.getenv()` directly. Never hardcode URLs or passwords. Always use `EnvManager`.

### 5.2 Fixtures — shared setup code

A **fixture** is a function that prepares something a test needs (e.g. a logged-in user,
a browser page, an API client). Fixtures are defined in `conftest.py` files.

```python
# tests/api/conftest.py
import pytest
from framework.api.auth_api import AuthAPI
from framework.env_manager import EnvManager

@pytest.fixture(scope="session")       # runs once for the whole test session
def auth_tokens(load_environment) -> dict:
    """Logs in and returns access tokens."""
    auth_api = AuthAPI()
    tokens = auth_api.authorization(
        email=EnvManager.get("USER_EMAIL_DEV"),
        password=EnvManager.get("USER_PASSWORD_DEV")
    )
    return tokens.json()
```

A test uses a fixture simply by naming it as a parameter:

```python
def test_something(self, auth_tokens):  # pytest injects auth_tokens automatically
    print(auth_tokens["accessToken"])
```

**Fixture scopes:**

| Scope | Runs | Use for |
|-------|------|---------|
| `session` | Once per entire test run | Authentication, shared read-only resources |
| `function` | Once per test | Anything that changes state |

> **Rule:** Always declare the scope explicitly. Never rely on the default.

### 5.3 conftest.py hierarchy

pytest automatically discovers `conftest.py` files from outer to inner folders.
This means fixtures defined higher up are available to all tests below them.

```
tests/conftest.py               ← available to ALL tests (browser, page, load_environment)
tests/api/conftest.py           ← available to all API tests (auth_tokens)
tests/api/epic_1_.../conftest.py ← available to tests in this epic only
```

### 5.4 The Allure base class pattern

Every test file defines a **private base class** (name starts with `_`) that carries
the three-level Allure label hierarchy. All test classes in the file inherit from it.

```python
@allure.parent_suite("API Tests")   # Level 1 — test type
@allure.suite("Registration")       # Level 2 — feature area
@allure.sub_suite("US-1.15 Exchange Rates")  # Level 3 — user story
class _ExchangeRatesBase:
    """Shared Allure hierarchy — do not add tests here."""


@allure.story("Status code and fields")  # Level 4 — story within the user story
@pytest.mark.qase("LP-422")
class TestExchangeRates(_ExchangeRatesBase):
    ...
```

The `_` prefix tells pytest: *this is not a test class, don't collect it*.

---

## 6. Writing Your First API Test

We will write a test for the **Exchange Rates** endpoint (`GET /api/processing-center/exchange-rates`).

### Step 1 — Create the folder structure

```
tests/api/epic_1_welcome_page/us_1_15_exchange_rates/
├── __init__.py          ← empty file, required by Python
└── test_exchange_rates.py
```

Create the empty `__init__.py`:
```bash
touch tests/api/epic_1_welcome_page/us_1_15_exchange_rates/__init__.py
```

### Step 2 — Create test data

Create `tests/api/epic_1_welcome_page/data/exchange_rates_data.py`:

```python
# Option B — Python data file
EXCHANGE_RATE_CASES = [
    {"name": "status_is_200",      "expected_status": 200},
    {"name": "rates_field_exists", "field": "rates"},
    {"name": "base_currency_pln",  "expected_base_currency": "PLN"},
]
```

### Step 3 — Write the test file

```python
# tests/api/epic_1_welcome_page/us_1_15_exchange_rates/test_exchange_rates.py

import allure
import pytest
from assertpy import assert_that

from framework.api.exchange_rates_api import ExchangeRatesAPI
from framework.env_manager import EnvManager

# Every test file must declare its module-level marker
pytestmark = [pytest.mark.api]


# ── Step A: Private base class with Allure hierarchy ──────────────────────────

@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.15 Exchange Rates")
class _ExchangeRatesBase:
    """Shared Allure labels for all exchange rate test classes."""


# ── Step B: Test class inheriting from base ───────────────────────────────────

@allure.story("GET exchange rates — happy path")
@pytest.mark.qase("LP-422")
@pytest.mark.smoke
class TestGetExchangeRates(_ExchangeRatesBase):

    # Step C: A setup fixture — runs before each test method in this class
    @pytest.fixture(scope="function", autouse=True)
    def _setup(self, exchange_rates_api):
        """Call the API once and store the response on self."""
        with allure.step("GET /api/processing-center/exchange-rates"):
            self.response = exchange_rates_api.get_exchange_rates()
            self.body = self.response.json()

    # Step D: Individual test methods — one behavior each

    @allure.title("Status code is 200 OK")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_status_code_is_200(self):
        assert_that(self.response.status_code) \
            .described_as("Status code") \
            .is_equal_to(200)

    @allure.title("Response body contains 'rates' field")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rates_field_present(self):
        assert_that(self.body) \
            .described_as("Response body") \
            .contains_key("rates")

    @allure.title("Base currency is PLN")
    @allure.severity(allure.severity_level.NORMAL)
    def test_base_currency_is_pln(self):
        assert_that(self.body["baseCurrency"]) \
            .described_as("baseCurrency field") \
            .is_equal_to("PLN")

    @allure.title("Rates list is not empty")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rates_list_is_not_empty(self):
        assert_that(self.body["rates"]) \
            .described_as("rates list") \
            .is_not_empty()
```

### What each part does

| Part | What it is | Why it matters |
|------|-----------|----------------|
| `pytestmark = [pytest.mark.api]` | Marks all tests in this file as API tests | Lets you run only API tests with `-m api` |
| `_ExchangeRatesBase` | Holds Allure labels | All test classes inherit these without repeating them |
| `@pytest.fixture autouse=True` | Runs before every test automatically | Avoids copy-pasting the API call in each test |
| `assert_that(...).described_as(...)` | assertpy assertion | The `described_as` message appears in the error if the test fails |
| `with allure.step(...)` | Labels a block in the Allure report | Makes the report readable — shows what happened step by step |

### Step 4 — Add the API fixture in conftest.py

The test uses `exchange_rates_api` — this fixture must exist in the epic's `conftest.py`:

```python
# tests/api/epic_1_welcome_page/conftest.py
import pytest
from framework.api.exchange_rates_api import ExchangeRatesAPI

@pytest.fixture(scope="session")
def exchange_rates_api(load_environment) -> ExchangeRatesAPI:
    """Returns an ExchangeRatesAPI client."""
    return ExchangeRatesAPI()
```

---

## 7. Writing Your First UI Test

We will write a UI test for the **Login page** that checks the page opens correctly
and the login button is disabled when fields are empty.

### Step 1 — Create the folder structure

```
tests/ui/epic_1_welcome_page/us_1_2_log_into_my_profile/
├── __init__.py
└── test_log_into_my_profile.py
```

### Step 2 — Create or check the Page Object

Page Objects live in `framework/ui/pages/`. They hold **all locators and actions** for a page.
Never put locators in test files.

```python
# framework/ui/pages/log_into_my_profile.py
from playwright.sync_api import Page, expect
from framework.ui.core.base_page import BasePage
from framework.env_manager import EnvManager


class SignInLocators:
    """All CSS/role locators for the login page — defined once, used everywhere."""
    LOGIN_NAV_BUTTON = "[data-testid='login-button']"
    EMAIL_INPUT      = "[data-testid='email-input']"
    PASSWORD_INPUT   = "[data-testid='password-input']"
    LOGIN_BUTTON     = "[data-testid='submit-button']"
    VALIDATION_ERROR = "[data-testid='validation-error']"
    GENERAL_ERROR    = "[data-testid='general-error']"


class LoginPage(BasePage):
    """Page Object for the Login page."""

    def __init__(self, page: Page):
        super().__init__(page, f"{EnvManager.get_config().base_url}/login")

    def open_login_page(self) -> None:
        """Navigate to home and click the Login nav button."""
        self.page.goto(EnvManager.get_config().base_url)
        self.page.locator(SignInLocators.LOGIN_NAV_BUTTON).click()

    def fill_email(self, value: str) -> None:
        self.page.locator(SignInLocators.EMAIL_INPUT).fill(value)

    def fill_password(self, value: str) -> None:
        self.page.locator(SignInLocators.PASSWORD_INPUT).fill(value)

    def click_login(self) -> None:
        self.page.locator(SignInLocators.LOGIN_BUTTON).click()

    def expect_login_button_disabled(self) -> None:
        expect(self.page.locator(SignInLocators.LOGIN_BUTTON)).to_be_disabled()

    def expect_login_button_enabled(self) -> None:
        expect(self.page.locator(SignInLocators.LOGIN_BUTTON)).to_be_enabled()

    def expect_validation_error(self, message: str) -> None:
        expect(self.page.locator(SignInLocators.VALIDATION_ERROR)).to_contain_text(message)
```

### Step 3 — Create test data

```python
# tests/ui/epic_1_welcome_page/data/log_into_my_profile_data.py

VALIDATION_CASES = [
    {
        "name":           "email_too_short",
        "email":          "a@b.c",
        "password":       "Valid@123!",
        "expected_error": "Must be between 6 and 55 characters",
    },
    {
        "name":           "invalid_email_format",
        "email":          "not-an-email",
        "password":       "Valid@123!",
        "expected_error": "Please enter a valid email address",
    },
]
```

### Step 4 — Write the test file

```python
# tests/ui/epic_1_welcome_page/us_1_2_log_into_my_profile/test_log_into_my_profile.py

import allure
import pytest
from playwright.sync_api import expect

from framework.ui.pages.log_into_my_profile import LoginPage, SignInLocators
from tests.ui.epic_1_welcome_page.data.log_into_my_profile_data import VALIDATION_CASES

pytestmark = [pytest.mark.ui]


# ── Allure base class ─────────────────────────────────────────────────────────

@allure.parent_suite("UI Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.2 Log Into My Profile")
class _LoginBase:
    """Shared Allure hierarchy for login page tests."""


# ── Test classes ──────────────────────────────────────────────────────────────

@allure.story("Login page opens correctly")
@pytest.mark.smoke
class TestLoginPageOpens(_LoginBase):

    @allure.title("Login page is accessible from the home page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_page_opens(self, page):
        login_page = LoginPage(page)

        with allure.step("Navigate to home page and click Login"):
            login_page.open_login_page()

        with allure.step("Assert URL changed to /login"):
            expect(page).to_have_url(f"{login_page.url}")

    @allure.title("Login button is disabled when both fields are empty")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_button_disabled_when_fields_empty(self, page):
        login_page = LoginPage(page)

        with allure.step("Open the login page"):
            login_page.open_login_page()

        with allure.step("Assert Login button is disabled"):
            login_page.expect_login_button_disabled()


@allure.story("Email field validation")
@pytest.mark.regression
class TestEmailValidation(_LoginBase):

    test_data_map = {"validation_case": VALIDATION_CASES}

    @allure.title("Validation error shown for invalid email — {validation_case}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_email_shows_error(self, page, validation_case):
        login_page = LoginPage(page)

        with allure.step("Open the login page"):
            login_page.open_login_page()

        with allure.step(f"Fill email: {validation_case['email']!r}"):
            login_page.fill_email(validation_case["email"])

        with allure.step(f"Fill password: {validation_case['password']!r}"):
            login_page.fill_password(validation_case["password"])

        with allure.step("Click away to trigger validation"):
            page.keyboard.press("Tab")

        with allure.step(f"Assert error: {validation_case['expected_error']!r}"):
            login_page.expect_validation_error(validation_case["expected_error"])

        with allure.step("Assert Login button is still disabled"):
            login_page.expect_login_button_disabled()
```

### Key differences between API and UI tests

| | API tests | UI tests |
|-|-----------|----------|
| Assertion library | `assertpy` — `assert_that(...).is_equal_to(...)` | Playwright — `expect(locator).to_be_visible()` |
| What you interact with | `requests.Response` objects | Browser elements via locators |
| Locators | Not needed | Defined in Page Object, never in tests |
| Waiting | Not needed (HTTP is synchronous) | Never use `wait_for_timeout()` — Playwright waits automatically |

---

## 8. Test Data

Test data lives in the `data/` folder inside each epic folder.
Two formats are allowed — pick one per feature.

### Option A — YAML file (`<feature>.yaml`)

```yaml
# tests/api/epic_1_welcome_page/data/first_name_cases.yaml
- name: valid_two_chars
  value: "Jo"
  expected_status: 201

- name: invalid_one_char
  value: "J"
  expected_status: 400

- name: invalid_empty
  value: ""
  expected_status: 400
```

Load it in your test file:
```python
import yaml

def _load_data() -> list:
    with open("tests/api/epic_1_welcome_page/data/first_name_cases.yaml") as f:
        return yaml.safe_load(f)

DATA = _load_data()
```

### Option B — Python file (`<feature>_data.py`)

```python
# tests/api/epic_1_welcome_page/data/first_name_data.py
FIRST_NAME_CASES = [
    {"name": "valid_two_chars",  "value": "Jo", "expected_status": 201},
    {"name": "invalid_one_char", "value": "J",  "expected_status": 400},
    {"name": "invalid_empty",    "value": "",   "expected_status": 400},
]
```

Import it in your test file:
```python
from tests.api.epic_1_welcome_page.data.first_name_data import FIRST_NAME_CASES
```

### Using test_data_map for parametrized tests

```python
class TestFirstName(_Base):
    test_data_map = {"first_name_case": FIRST_NAME_CASES}

    @allure.title("First name validation — {first_name_case}")
    def test_first_name(self, first_name_case):
        # first_name_case is one dict from the list, e.g. {"name": "valid_two_chars", ...}
        r = api.submit(first_name=first_name_case["value"])
        assert_that(r.status_code).is_equal_to(first_name_case["expected_status"])
```

pytest runs this test **once per entry** in `FIRST_NAME_CASES`, using the `name` field as the test ID.

### Rules for test data entries

- Every entry **must** have a `name` field (lowercase with underscores)
- Cover three types: **happy path** (valid input), **negative** (invalid input), **edge case** (boundary values)
- Never put raw data inline inside a test method

---

## 9. Running Tests

All commands must be run from the project root folder (`web-autotests/`).

```bash
# Run all tests against the dev environment
poetry run pytest tests/ --env=dev

# Run only API tests
poetry run pytest -m api --env=dev

# Run only UI tests
poetry run pytest -m ui --env=dev

# Run only smoke tests (fast critical path)
poetry run pytest -m smoke --env=dev

# Run a single test file
poetry run pytest tests/api/epic_1_welcome_page/us_1_15_exchange_rates/test_exchange_rates.py --env=dev

# Run tests in parallel (4 workers — matches CI)
poetry run pytest -n 4 --env=dev

# Run a single test by name
poetry run pytest tests/ --env=dev -k "test_status_code_is_200"
```

### Understanding test output

```
PASSED  tests/api/epic_1_welcome_page/us_1_15_exchange_rates/test_exchange_rates.py::TestGetExchangeRates::test_status_code_is_200
FAILED  tests/api/...::test_base_currency_is_pln
SKIPPED tests/api/...::test_user_blocked_after_5_failed
```

- **PASSED** ✅ — test ran and all assertions passed
- **FAILED** ❌ — test ran but an assertion failed (or an error occurred)
- **SKIPPED** ⚠️ — test was intentionally skipped (`@pytest.mark.skip` or `pytest.skip()`)

---

## 10. Viewing the Allure Report

After running tests, an `allure-results/` folder is created automatically.
To view the report in your browser:

```bash
# Start a local Allure server (opens the browser automatically)
allure serve allure-results
```

If `allure` is not installed:
```bash
# macOS with Homebrew
brew install allure
```

### What you will see in the report

- **Suites** view — tests grouped by parent suite → suite → sub-suite → story
- **Each test** shows its steps, attachments (request/response JSON), severity, and duration
- **Failed tests** show the exact assertion that failed with the `described_as` message

---

## 11. Common Mistakes to Avoid

### ❌ Mistake 1 — Using `@pytest.mark.parametrize` for data-driven tests

```python
# WRONG ❌
@pytest.mark.parametrize("value,expected", [("Jo", 201), ("J", 400)])
def test_first_name(self, value, expected):
    ...
```

```python
# CORRECT ✅ — use test_data_map
class TestFirstName(_Base):
    test_data_map = {
        "first_name_case": [
            {"name": "valid_two_chars",  "value": "Jo", "expected_status": 201},
            {"name": "invalid_one_char", "value": "J",  "expected_status": 400},
        ]
    }

    def test_first_name(self, first_name_case):
        ...
```

**Why:** `test_data_map` gives readable test IDs, integrates with Allure titles automatically,
and is the convention the whole team follows.

---

### ❌ Mistake 2 — Hardcoding URLs or credentials

```python
# WRONG ❌
page.goto("https://dev.example.com")
auth_api.login(email="user@example.com", password="Pass123!")
```

```python
# CORRECT ✅
page.goto(EnvManager.get_config().base_url)
auth_api.login(
    email=EnvManager.get("USER_EMAIL_DEV"),
    password=EnvManager.get("USER_PASSWORD_DEV")
)
```

**Why:** Hardcoded values break when switching environments and expose credentials in the codebase.

---

### ❌ Mistake 3 — Putting locators in test files

```python
# WRONG ❌
def test_login(self, page):
    page.locator("[data-testid='email-input']").fill("user@example.com")
    page.locator("[data-testid='submit-button']").click()
```

```python
# CORRECT ✅ — locators live in the Page Object
def test_login(self, page):
    login_page = LoginPage(page)
    login_page.fill_email("user@example.com")
    login_page.click_login()
```

**Why:** When the UI changes, you fix the locator in one place (the Page Object),
not in every test that uses it.

---

### ❌ Mistake 4 — Using `wait_for_timeout()` in UI tests

```python
# WRONG ❌
page.wait_for_timeout(3000)  # sleep for 3 seconds
expect(page.locator(".result")).to_be_visible()
```

```python
# CORRECT ✅ — Playwright waits automatically
expect(page.locator(".result")).to_be_visible()  # waits up to the default timeout
```

**Why:** Fixed sleeps make tests slow and flaky. Playwright's `expect()` polls until
the condition is met or times out — no sleep needed.

---

### ❌ Mistake 5 — Writing a standalone test function (not in a class)

```python
# WRONG ❌
def test_exchange_rates():
    ...
```

```python
# CORRECT ✅
class TestExchangeRates(_Base):
    def test_exchange_rates(self):
        ...
```

**Why:** The Allure base class pattern only works with classes. Standalone functions
also can't use the `test_data_map` mechanism.

---

### ❌ Mistake 6 — Putting assertions inside fixtures

```python
# WRONG ❌
@pytest.fixture(scope="session")
def auth_tokens(load_environment):
    tokens = auth_api.authorization(...)
    assert tokens.status_code == 200  # ← assertion in fixture!
    return tokens.json()
```

```python
# CORRECT ✅
@pytest.fixture(scope="session")
def auth_tokens(load_environment):
    tokens = auth_api.authorization(...)
    if tokens.status_code != 200:
        raise RuntimeError(f"Login failed: {tokens.status_code} {tokens.text}")
    return tokens.json()
```

**Why:** Assertions in fixtures produce confusing error messages. Raise `RuntimeError`
with a clear message instead so it's obvious the problem is in setup, not in the test itself.

---

### ❌ Mistake 7 — Using `os.getenv()` for secrets

```python
# WRONG ❌
import os
email = os.getenv("USER_EMAIL_DEV")
```

```python
# CORRECT ✅
from framework.env_manager import EnvManager
email = EnvManager.get("USER_EMAIL_DEV")
```

**Why:** `EnvManager.get()` raises a clear `RuntimeError` if the variable is missing,
instead of silently returning `None` and causing a cryptic failure later.

---

### ❌ Mistake 8 — Missing `described_as()` on assertpy assertions

```python
# WRONG ❌
assert_that(response.status_code).is_equal_to(200)
# Failure: Expected <200> but was <400>  ← which field? which test step?
```

```python
# CORRECT ✅
assert_that(response.status_code) \
    .described_as("POST /registration/personal-info status code") \
    .is_equal_to(200)
# Failure: [POST /registration/personal-info status code] Expected <200> but was <400>
```

**Why:** The `described_as` label appears in the failure message and in the Allure report,
making it immediately obvious what failed and why.

---

## Quick Reference Card

```
New test checklist:
  ✅ Created in tests/  (not in framework/)
  ✅ Inside a class that inherits from _<Name>Base
  ✅ One test method = one behavior
  ✅ File named test_<feature>.py
  ✅ pytestmark = [pytest.mark.api] or [pytest.mark.ui]
  ✅ @allure.title() on every test method
  ✅ @allure.severity() on every test method
  ✅ Every action inside with allure.step()
  ✅ assertpy used for API, expect() used for UI
  ✅ .described_as() on every assertpy assertion
  ✅ No hardcoded URLs or passwords
  ✅ No locators inside test files (UI tests)
  ✅ No wait_for_timeout() (UI tests)
  ✅ Test data in data/ folder, not inline
  ✅ Every data entry has a "name" field
```
