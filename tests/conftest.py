import os
import shutil


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