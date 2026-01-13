# PRetty-autotests

UI + API Test Automation | Python • Pytest • Playwright • Poetry

This repository contains a learning-oriented but production-style Automation QA framework for UI and API testing, designed for company internal use and for Automation Engineers who want a clean, scalable, and easy-to-understand solution.
The framework combines Playwright for UI automation, Pytest for test execution, and Poetry for dependency management, following best industry practices while remaining beginner‑friendly.

📌 Why This Framework?

This framework was created to:

Learn and apply real-world automation architecture

Provide a single solution for UI and API testing

Demonstrate best practices suitable for internal company projects

Be easy to onboard for new Automation Engineers

Scale from simple tests to complex test suites

Key principles: 

✅ Readability over complexity

✅ Explicit configuration

✅ Reusability and maintainability

## Getting started

Need setup next files - config, framework



## Framework Setup on local machine
    1. Enable two-factor authentication
        a. Goto git
        b. Click on your profile avatar
        c. Click on edit profile 
        d. Click on Account
        e. Enable to two-facto authentication
    2. Configure Oauth using instruction mentioned in  https://docs.gitlab.com/integration/oauth_provider/ ( redirect URI is http://127.0.0.1/ ) and copy application id and secret code.
    3. Clear any old configuration (if required) using executing below commands on terminal
        a. git config --global --unset-all credential.https://git.andersenlab.com.gitLabDevClientId
        b.  git config --global --unset-all credential.https://git.andersenlab.com.gitLabDevClientSecret
        c. git config --global --unset-all credential.https://git.andersenlab.com.provider
    4. Now, configure the setup by running below commands on terminal.
        a. git config --global credential.https://git.andersenlab.com.gitLabDevClientId <application id>
        b. git config --global credential.https://git.andersenlab.com.gitLabDevClientSecret <secret code>
    5. Clone the Pretty-autotests repository using below command on terminal
        a. git clone <repository url>

## Requirements:
* Python 3.11, NOT lower.
* Install Poetry - pip install poetry
* Setup requirements - poetry install
* Install required browsers for playwright - playwright install
* Activation pre-commit - pre-commit install

## Database connection instruction:
To connect to DB follow next steps:
https://wiki.andersenlab.com/spaces/PRETTY02/pages/447447438/Database+connection+instruction

## Configuration & Environments
The framework supports multiple environments:

* dev
* test
* prod

Configuration files are stored in the config/ directory and written in YAML / JSON.

Example (config/test.yaml):

base_url: https://test.example.com

api_url: https://api.test.example.com

browser: chromium

headless: true

#  UI Tests

Automated UI tests for a web application built with pytest, Playwright, and Allure, following the Page Object Model (POM) pattern.

# Tech Stack

* Python 3.11+
* pytest — testing framework 
* Playwright — browser automation
* Allure — test reporting
* Qase — test management (via markers)
* Page Object Model (POM) — test architecture pattern

## Project Structure (example)

```text
project/
│
├── framework/
│   └── ui/
│       └── pages/
│           └── example_page.py
│
├── tests/
│   └── example.spec.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

## Architecture

The project follows the Page Object Model (POM) approach:
* page logic is encapsulated in ExamplePage
* tests contain only high-level actions
* UI locators and interactions are not duplicated and stored in exact page class

 How to Add a New Page Object:

* Create a new file in src/pages
* Inherit from BasePage
* Keep locators and actions inside the page class only

# API Tests
## Technologies & Tools

- **Python**
- **pytest** — test framework
- **Allure** — test reporting
- **Qase** — test case management
- **REST API**

## Authentication

The test requires valid authentication tokens.

A pytest fixture `get_tokens` is used to obtain the required authorization tokens.
Fixtures are stored in api\conftest.py

# Database Client Tests

## Technologies & Tools

- **Python**
- **pytest**
- **SQLAlchemy**
- **PostgreSQL**
- **python-dotenv**
- **poetry** (for running tests)

## Environment Configuration

The database connection is configured using environment variables loaded from a `.env` file:
```env
DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
```

The connection string is built dynamically:
postgresql://DB_USER:DB_PASS@DB_HOST:DB_PORT/DB_NAME

Make sure:

* the database is running
* credentials are correct
* test data exists or is expected to appear during execution

## How to Add New Tests
Create a new test file under tests/ui or tests/api
Use existing fixtures (page, authenticated_user, test_data)
Apply markers if needed

## Markers Used
* `@pytest.mark.api` — marks the test as an API test
* `@pytest.mark.ui` — UI test marker
* `@pytest.mark.qase("US-1.1")` — link to Qase test case
* `@allure.suite("Example UI Tests")` — Allure test suite
* `@allure.severity(NORMAL)` — test severity level

## Run tests:
* Run one test: "pytest tests/<module_name>/<test_name>"
* Run all tests: "pytest tests/"
* Run using pytest-xdist: "pytest -n <n>"
* Run all UI tests: "pytest -m ui"
* View Allure report: "allure serve allure-results"
* Run the test manually via pytest: poetry run pytest path/to/test_file.py

## Target Audience

* Automation QA Engineers
* Engineers onboarding into UI/API automation
* Internal QA teams

## License

Internal company project / learning framework.

