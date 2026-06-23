class AddressLocators:
    # Registration Address
    REGISTRATION_STREET = "#registrationAddress\\.street"
    REGISTRATION_HOUSE_NUMBER = "#registrationAddress\\.houseNumber"
    REGISTRATION_APARTMENT = "#registrationAddress\\.apartment"
    REGISTRATION_POSTAL_CODE = "#registrationAddress\\.postalCode"
    REGISTRATION_CITY = "#registrationAddress\\.city"

    # Shared controls
    BILLING_SAME_AS_REGISTRATION_CHECKBOX = "input[name='billingSameAsRegistration']"
    CONTINUE_BUTTON = "button:has-text('Continue')"


class AddressPage:
    def __init__(self, page):
        self.page = page

    # ── Registration Address ─────────────────────────────────────────────────

    def fill_registration_street(self, street):
        self.page.locator(AddressLocators.REGISTRATION_STREET).fill(street)

    def fill_registration_house_number(self, house_number):
        self.page.locator(AddressLocators.REGISTRATION_HOUSE_NUMBER).fill(house_number)

    def fill_registration_apartment(self, apartment):
        self.page.locator(AddressLocators.REGISTRATION_APARTMENT).fill(apartment)

    def fill_registration_postal_code(self, postal_code):
        self.page.locator(AddressLocators.REGISTRATION_POSTAL_CODE).fill(postal_code)

    def fill_registration_city(self, city):
        # City is a combobox — after typing, a dropdown with suggestions appears.
        # We type the city name and press Enter to confirm the value.
        self.page.locator(AddressLocators.REGISTRATION_CITY).fill(city)
        self.page.keyboard.press("Enter")

    def fill_registration_address(self, street, house_number, apartment, postal_code, city):
        """Convenience method — fills all Registration Address fields in one call."""
        self.fill_registration_street(street)
        self.fill_registration_house_number(house_number)
        self.fill_registration_apartment(apartment)
        self.fill_registration_postal_code(postal_code)
        self.fill_registration_city(city)

    # ── Shared controls ───────────────────────────────────────────────────────

    def check_billing_same_as_registration(self):
        self.page.locator(AddressLocators.BILLING_SAME_AS_REGISTRATION_CHECKBOX).check()

    def click_continue(self):
        self.page.locator(AddressLocators.CONTINUE_BUTTON).click()
