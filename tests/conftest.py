import os
import shutil
import pytest

from framework.logger.logger import Logger
from framework.env_manager import EnvManager
from framework.utils.utils import get_root_dir

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
    Loads environment variables from the correct .env.dev.<env> file
    before any tests are executed.
    """
    env = request.config.getoption("--env")
    EnvManager.load(env)


def pytest_configure(config):

    allure_dir = get_root_dir() / "allure-results"

    if allure_dir.is_dir():
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
