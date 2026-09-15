import uuid

import pytest

from framework.ui.pages.address_page import AddressPage
from framework.ui.pages.sign_up.personal_info_page import PersonalInfoPage


def _unique_passport() -> str:
    return f"BR{uuid.uuid4().hex[:7].upper()}"


@pytest.fixture
def address_page(page):
    """
    Navigates through steps 1 and 2 so that tests start directly on the Address page (step 3).
    Uses unique passport per run to avoid duplicate-passport errors.
    """
    # ── Step 1: Personal Info ────────────────────────────────────────────────
    personal_info = PersonalInfoPage(page)
    personal_info.open()
    personal_info.fill_required_fields(
        first_name="Ivan",
        last_name="Petrov",
        passport_id=_unique_passport(),
        birth_date="01/01/1980",
    )
    personal_info.click_continue()

    # ── Step 2: Contact Info ─────────────────────────────────────────────────
    # ContactInfoPage is not yet implemented; using direct locators for now.
    # Switch to ContactInfoPage methods once the page object is ready.
    page.get_by_label("Email").press_sequentially("example@gmail.com")
    page.get_by_label("Phone number").press_sequentially("+359881234567")
    page.get_by_role("button", name="Continue").click()

    return AddressPage(page)
