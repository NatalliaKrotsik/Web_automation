from playwright.sync_api import Page, expect
from framework.env_manager import EnvManager
from framework.ui.core.base_page import BasePage


class PersonalInfoPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page, f"{EnvManager.get_config().base_url}/sign-up")

    # Locators 

    def first_name_input(self):
        return self.page.get_by_label("First Name") 

    def middle_name_input(self):
        return self.page.get_by_label("Middle Name")

    def last_name_input(self):
        return self.page.get_by_label("Last Name")

    def passport_id_input(self):
        return self.page.get_by_label("Passport ID")

    def birth_date_input(self):
        return self.page.get_by_placeholder("DD/MM/YYYY")

    def continue_button(self):
        return self.page.get_by_role("button", name="Continue")

    def back_button(self):
        return self.page.get_by_role("button", name="Back to personal info")
    
    def page_heading(self):
        return self.page.get_by_role("heading", name="Personal Information")

    def field_error(self, field_name: str):
        if field_name == "birthDate":
            return self.page.locator(
                "//input[@placeholder='DD/MM/YYYY']"
                "/ancestor::div[2]"
                "/span[contains(@class,'text-text-errorBody')]"
            )
        return self.page.locator(
            f"//input[@id='{field_name}']"
            "/ancestor::div[2]"
            "/span[contains(@class,'text-text-errorBody')]"
        )
    
    # ── Actions 

    def fill_first_name(self, value: str) -> None:
        self.first_name_input().fill(value)

    def fill_middle_name(self, value: str) -> None:
        self.middle_name_input().fill(value)

    def fill_last_name(self, value: str) -> None:
        self.last_name_input().fill(value)

    def fill_passport_id(self, value: str) -> None:
        self.passport_id_input().fill(value)

    def fill_birth_date(self, value: str) -> None:
        self.birth_date_input().fill(value)
        self.page.keyboard.press("Escape")

    def click_continue(self) -> None:
        self.continue_button().click()
    
    def click_back(self) -> None:
        self.back_button().click()

    def fill_required_fields(
        self,
        first_name: str,
        last_name: str,
        passport_id: str,
        birth_date: str,
    ) -> None:
        """Fills all required fields with valid data. Middle name is optional and skipped."""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_passport_id(passport_id)
        self.fill_birth_date(birth_date)

    def expect_page_heading_visible(self) -> None:
        expect(self.page_heading()).to_be_visible()

    def expect_all_fields_visible(self) -> None:
        expect(self.first_name_input()).to_be_visible()
        expect(self.middle_name_input()).to_be_visible()
        expect(self.last_name_input()).to_be_visible()
        expect(self.passport_id_input()).to_be_visible()
        expect(self.birth_date_input()).to_be_visible()

    def expect_continue_button_disabled(self) -> None:
        expect(self.continue_button()).to_be_disabled()

    def expect_continue_button_enabled(self) -> None:
        expect(self.continue_button()).to_be_enabled()

    def expect_field_error_visible(self, field_name: str, message: str) -> None:
        error = self.field_error(field_name)
        expect(error).to_be_visible()
        expect(error).to_have_text(message)

    def expect_field_value(self, field_id: str, value: str) -> None:
        if field_id == "birthDate":
            expect(self.birth_date_input()).to_have_value(value)
        else:
            expect(self.page.locator(f"//input[@id='{field_id}']")).to_have_value(value)