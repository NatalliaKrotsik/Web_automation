import allure
import pytest

pytestmark = [pytest.mark.api]


@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.11 ATM & Branch Locations")
class _ATMBase:
    """Shared Allure hierarchy for ATM/branch location test classes."""
