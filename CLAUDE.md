# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI + API + DB test automation framework for **PrettyBank** — an internal banking web application. Uses Playwright for UI, `requests` for API, SQLAlchemy for DB, pytest for test execution, Allure for reporting, and Qase for test management.

## Commands

```bash
# Install dependencies
poetry install
playwright install chromium

# Activate pre-commit hooks (required once after clone)
pre-commit install

# Run all tests
poetry run pytest tests/ --env=test

# Run a single test file
poetry run pytest tests/api/epic_1_welcome_page/us_1_1_3_input_address_info/test_address_info.py --env=test

# Run by type marker
poetry run pytest -m api --env=test
poetry run pytest -m ui --env=test

# Parallel run (matches CI configuration)
poetry run pytest -n 4 --env=test

# View Allure report locally
allure serve allure-results

# Lint and format
poetry run ruff check .
poetry run black .
```

Available `--env` values: `dev`, `test`, `prod`. Defaults to `test`.

## Architecture

### Configuration (`framework/env_manager.py`)

`EnvManager` is a session-scoped singleton. It loads `configs/<env>.yaml` (URLs, browser settings, timeouts) and secrets from `env/.env.<env>` (not committed). Access config anywhere via `EnvManager.get_config()` or secrets via `EnvManager.get("VAR_NAME")`.

Required `.env` variables:
- `USER_EMAIL_DEV`, `USER_PASSWORD_DEV` — regular user credentials
- `ADMIN_USER_EMAIL`, `ADMIN_USER_PASSWORD` — admin credentials
- `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME` — database connection

### API Layer (`framework/api/`)

`HttpClient` (base class) handles URL building, `requests.Session`, and automatic Allure attachment of request/response details. All API classes inherit from it:

```
HttpClient
├── AuthAPI       → api/auth/sign-in, sign-out, session/ping
├── PersonalDataAPI
├── AddressAPI    → api/registration/address
└── ExchangeRatesAPI
```

### UI Layer (`framework/ui/`)

Page Object Model:
- `BasePage` — wraps Playwright `Page`: `open()`, navigation helpers, clipboard utility
- `BaseElement` — wraps a locator with common interactions
- Specific pages (`login_page.py`, `home_page.py`, `sign_up/personal_info_page.py`, etc.) inherit from `BasePage`

### Database Layer (`framework/data_base/db_client.py`)

`DbClient` uses SQLAlchemy Core against a PostgreSQL `public.user_user` table. Provides `user_exists()`, `get_user_data()`, and `wait_until_user_created()` (polling up to 30s).

### Test Structure

```
tests/
├── conftest.py                     # session fixtures: env loading, browser/page, Allure label MRO propagation
├── api/
│   ├── conftest.py                 # auth_tokens + admin_auth_tokens (session-scoped)
│   ├── epic_1_welcome_page/
│   │   ├── conftest.py             # api + valid_payload fixtures; loads YAML test data
│   │   ├── data/                   # YAML/Python test data files
│   │   └── us_1_1_*/              # one folder per user story
└── ui/
    ├── conftest.py
    └── epic_1_welcome_page/
        └── us_1_1_*/
```

Tests are **class-based** with `@pytest.mark.api` / `@pytest.mark.ui`. Authentication is handled via session-scoped `auth_tokens` fixture — never instantiate `AuthAPI` inside a test directly.

### Parametrization Pattern

Define `test_data_map` on a test class, and `conftest.pytest_generate_tests` will auto-parametrize matching fixture names. Test case names come from a `"name"` key in each dict.

### Allure Labels

Apply `@allure_label` markers on the **class** — the MRO-walking hook in `tests/conftest.py` propagates them to all test methods automatically. No need to repeat labels per method.

## CI/CD

GitLab CI (`.gitlab-ci.yml`) runs `ui_tests` and `api_tests` in parallel with 4 workers, then merges Allure results and deploys to GitLab Pages. Allure history is preserved across pipelines via artifact download from `main`.
