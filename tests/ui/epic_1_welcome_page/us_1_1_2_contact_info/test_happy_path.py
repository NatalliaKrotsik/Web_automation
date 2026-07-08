import allure
import pytest

pytestmark = [pytest.mark.ui]


@allure.parent_suite("UI Tests")
@allure.suite("Registration")
@allure.sub_suite("US-1.1.2 Contact Info")
class _ContactInfoBase:
    """Shared Allure hierarchy for contact info test classes."""


@allure.story("Happy path")
class TestContactInfoHappyPath(_ContactInfoBase):

    @allure.title("TC-80 — Full valid contact info submission proceeds to next step")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.skip(reason="Not implemented yet")
    def test_full_valid_contact_info_submission(self, page):
        pass
