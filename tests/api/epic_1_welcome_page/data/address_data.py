valid_address = {
    "registrationAddress": {
        "street": "Prosta",
        "houseNumber": "1",
        "apartment": "15",
        "country": "Poland",
        "postalCode": "00-001",
        "city": "Warszawa",
        "type": "registration",
    },
    "billingAddress": {
        "street": "Prosta",
        "houseNumber": "1",
        "apartment": "15",
        "country": "Poland",
        "postalCode": "00-001",
        "city": "Warszawa",
        "type": "billing",
    },
    "billingSameAsRegistration": True,
}

# Street name validation rules:
# - no more than 60 characters
# - every word must be no more than 20 characters
# - must contain at least 1 letter (cannot consist of numbers only)
# - no less than 3 characters
# - only Latin letters, Polish national characters (ć, ń, ó, ś, ź, ż, ą, ę, ł), numbers
# - dash/hyphen (-) allowed but not as first/last symbol
# - whitespaces allowed but not as first/last symbol
invalid_streets = [
    "",  # empty
    "12",  # only numbers, less than 3 chars
    "ab",  # less than 3 chars
    "-Prosta",  # starts with hyphen
    "Prosta-",  # ends with hyphen
    " Prosta",  # leading space
    "Prosta ",  # trailing space
    "Main@Street",  # special character (@)
    "A" * 61,  # more than 60 chars
    "ABCDEFGHIJKLMNOPQRSTU",  # word > 20 chars
    "123",  # only numbers
    "Main#Street",  # special character (#)
    "Główna$123",  # special character ($)
    "Street@",  # special character at end
]

# House number validation rules:
# - digits, letters allowed
# - no less than 1 character
# - no more than 7 characters
# - "/" and "-" no more than 1 occurrence each
invalid_house_numbers = [
    "",  # empty
    "12345678",  # > 7 chars
    "12//3",  # more than one /
    "12--3",  # more than one -
    "@12",  # special character (@)
    "12#",  # special character (#)
    "1/2-3/4",  # multiple / and -
]

# Apartment/Flat number validation rules:
# - digits, letters allowed
# - no less than 1 character
# - no more than 7 characters
# - "/" and "-" NOT allowed
invalid_apartments = [
    "",  # empty
    "12345678",  # > 7 chars
    "@12",  # special character (@)
    "12#",  # special character (#)
    "12/3",  # "/" not allowed
    "12-3",  # "-" not allowed
    "A/B",  # "/" not allowed
    "A-B",  # "-" not allowed
]

# Postal code validation rules:
# - format XX-XXX where X is digit (0-9)
# - exactly 6 characters including hyphen
# - must correspond to the city
invalid_postal_codes = [
    "",  # empty
    "12345",  # no hyphen
    "123456",  # no hyphen
    "12-34",  # wrong format (should be XX-XXX)
    "12-3456",  # wrong format (too many digits after hyphen)
    "1A-234",  # letter in first part
    "AA-AAA",  # letters instead of digits
    "12_345",  # underscore instead of hyphen
    "12 345",  # space instead of hyphen
    "00-00",  # wrong format (should be XX-XXX with 3 digits after hyphen)
    "-00-001",  # starts with hyphen
    "00-001-",  # ends with hyphen
]

# City validation rules:
# - Latin letters only, including Polish national characters (ć, ń, ó, ś, ź, ż, ą, ę, ł)
# - no less than 3 characters
# - no more than 40 characters
# - can consist of 2 words (with space or hyphen)
invalid_cities = [
    "",  # empty
    "ab",  # less than 3 chars
    "A" * 41,  # more than 40 chars
    "123",  # only numbers
    "Warszawa123",  # contains numbers
    "@Warszawa",  # special character (@)
    "City!",  # special character (!)
    "War$",  # special character ($)
    "Kraków#2",  # special character (#) and numbers
]

# Postal code and city mismatch validation
# Postal code must correspond to the city
postal_city_mismatch = [
    {
        "postalCode": "80-001",
        "city": "Warszawa",
    },
    {
        "postalCode": "00-001",
        "city": "Gdansk",
    },
]
