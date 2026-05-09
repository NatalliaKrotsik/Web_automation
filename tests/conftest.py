import os
import shutil
import pytest

from framework.logger.logger import Logger
from framework.env_manager import EnvManager
from playwright.sync_api import sync_playwright



def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment: dev, test, prod"
    )


@pytest.fixture(scope="session", autouse=True)
def load_environment(request):
    """
    Loads environment variables from the correct .env.<env> file
    before any tests are executed.
    """
    env = request.config.getoption("--env")
    EnvManager.load(env)


def pytest_configure(config):
    """
    Cleans allure-results directory before test execution.
    """
    test_target = None
    for arg in config.args:
        candidate = arg.split("::", 1)[0]
        if os.path.isfile(candidate):
            test_target = os.path.abspath(candidate)
            break

    clean_dir = (
        os.path.dirname(test_target)
        if test_target
        else str(config.invocation_dir)
    )

    allure_dir = os.path.join(clean_dir, "allure-results")

    if os.path.isdir(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"[allure-cleanup] removed '{allure_dir}'")
        except Exception as e:
            print(f"[allure-cleanup] FAILED: {e}")
    else:
        print("[allure-cleanup] no allure-results directory found")


def pytest_runtest_logreport(report):
    """
    Logs test results using the framework logger.
    """
    if report.when == "call":
        logger = Logger.get_logger()
        nodeid = report.nodeid

        if report.passed:
            logger.logger.info(f"{nodeid} PASSED")
        elif report.failed:
            logger.error(f"{nodeid} FAILED")
        elif report.skipped:
            logger.logger.warning(f"{nodeid} SKIPPED")


def pytest_generate_tests(metafunc):
    """
    Dynamic parametrization from class-level test_data_map.
    """
    cls = metafunc.cls
    if not cls or not hasattr(cls, "test_data_map"):
        return

    for arg in metafunc.fixturenames:
        if arg in cls.test_data_map:
            data_list = cls.test_data_map[arg]
            ids = [
                item.get("name", str(item)) if isinstance(item, dict) else str(item)
                for item in data_list
            ]
            metafunc.parametrize(arg, data_list, ids=ids)

@pytest.fixture(scope="session")
def browser(load_environment):      # depends on load_environment so env loads first
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()