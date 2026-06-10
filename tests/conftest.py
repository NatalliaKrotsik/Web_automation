import shutil
import allure
import pytest

from framework.logger.logger import Logger
from framework.env_manager import EnvManager
from framework.utils.utils import get_root_dir
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


_ALLURE_LABEL_MAP = {
    "parentSuite": allure.dynamic.parent_suite,
    "suite":       allure.dynamic.suite,
    "subSuite":    allure.dynamic.sub_suite,
    "story":       allure.dynamic.story,
    "feature":     allure.dynamic.feature,
}


def pytest_runtest_setup(item):
    cls = getattr(item, "cls", None)
    if cls is None:
        return

    existing = {
        m.kwargs.get("label_type")
        for m in item.iter_markers("allure_label")
    }

    for klass in reversed(cls.__mro__):
        for marker in getattr(klass, "pytestmark", []):
            if marker.name == "allure_label":
                label_type = marker.kwargs.get("label_type")
                if label_type in _ALLURE_LABEL_MAP and label_type not in existing:
                    item.stash.setdefault("_allure_mro_labels", {})[label_type] = (
                        marker.args[0] if marker.args else None
                    )


@pytest.fixture(autouse=True)
def _apply_mro_allure_labels(request):
    labels = request.node.stash.get("_allure_mro_labels", {})
    for label_type, value in labels.items():
        if value and label_type in _ALLURE_LABEL_MAP:
            _ALLURE_LABEL_MAP[label_type](value)


def pytest_runtest_logreport(report):
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
def browser(load_environment):
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