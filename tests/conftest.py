import os
import shutil

from framework.logger.logger import Logger


def pytest_configure(config):
    """
    Before any tests are collected, determine whether you passed in
    a filename (via PyCharm’s green arrow or via the CLI). If so,
    clean that file’s directory; otherwise clean the invocation dir.
    """
    test_target = None
    for arg in config.args:
        candidate = arg.split("::", 1)[0]
        if os.path.isfile(candidate):
            test_target = os.path.abspath(candidate)
            break

    if test_target:
        clean_dir = os.path.dirname(test_target)
    else:
        clean_dir = str(config.invocation_dir)

    allure_dir = os.path.join(clean_dir, "allure-results")

    if os.path.isdir(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"[allure-cleanup] removed '{allure_dir}'")
        except Exception as e:
            print(f"[allure-cleanup] FAILED to remove '{allure_dir}': {e}")
    else:
        print(f"[allure-cleanup] no '{allure_dir}' directory found")


def pytest_runtest_logreport(report):
    """
    Logs test outcomes (PASSED/FAILED/SKIPPED/ERROR) using the new Logger.
    This replaces print statements with structured logging.
    """
    if report.when == "call":
        logger = Logger.get_logger()
        nodeid = report.nodeid 

        if report.passed:
            logger.logger.info(f"\033[92m{nodeid} PASSED\033[0m")
        elif report.failed:
            if hasattr(report, "longrepr"):
                logger.error(f"\033[91m{nodeid} FAILED\033[0m")
            else:
                logger.error(f"\033[91m{nodeid} FAILED\033[0m")
        elif report.skipped:
            logger.logger.warning(f"\033[93m{nodeid} SKIPPED\033[0m")
        elif report.outcome == "error":
            logger.error(f"\033[91m{nodeid} ERROR\033[0m")


def pytest_generate_tests(metafunc):
    for arg in metafunc.fixturenames:
        if arg in metafunc.cls.__dict__.get("test_data_map", {}):
            data_list = metafunc.cls.test_data_map[arg]
            ids = []
            for item in data_list:
                if isinstance(item, dict) and "name" in item:
                    ids.append(item["name"])
                else:
                    ids.append(str(item))

            metafunc.parametrize(arg, data_list, ids=ids)