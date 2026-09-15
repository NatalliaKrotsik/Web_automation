import pytest

VALID_EMAILS = [
    pytest.param("john.doe@gmail.com", id="valid_email_with_dot"),
    pytest.param("john_doe@gmail.com", id="valid_email_with_underscore"),
    pytest.param("john-doe@gmail.com", id="valid_email_with_hyphen"),
    pytest.param("example@box.com", id="valid_email_com_domain"),
    pytest.param("example@box.by", id="valid_email_by_domain"),
    pytest.param("example@box.ru", id="valid_email_ru_domain"),
    pytest.param("example@box.LOL", id="valid_email_uppercase_tld"),
    pytest.param("m@k.by", id="valid_email_6_characters"),
    pytest.param("mr@k.by", id="valid_email_7_characters"),
    pytest.param(
        "wiitkzpxunlvevrjvvzgipryalytmbnkmqxzhzztxekoqucb@a.vtp",
        id="valid_email_56_characters",
    ),
    pytest.param(
        "wiitkzpxunlvevrjvvzgipryalytmbnkmqxzhzzttxekoqucb@a.vtp",
        id="valid_email_55_characters",
    ),
    pytest.param("EXAMPLE@BOX.COM", id="valid_email_uppercase"),
    pytest.param("example@box.com", id="valid_email_lowercase"),
    pytest.param("eXamPle@box.com", id="valid_email_mixcase"),
]


INVALID_EMAILS = [
    pytest.param(
        {
            "email": "john!@gmail.com",
            "expected_error": "Email wrong format",
        },
        id="contains the special character " "!",
    ),
    pytest.param(
        {
            "email": " jo?hn@gmail.com",
            "expected_error": "Email wrong format",
        },
        id="contains the special character " "?",
    ),
    pytest.param(
        {
            "email": "john\\doe@gmail.com",
            "expected_error": "Email wrong format",
        },
        id="contains_backslash_character",
    ),
    pytest.param(
        {
            "email": "email2mailbox.com",
            "expected_error": "Email wrong format. try adding a '@' symbol",
        },
        id="email without '@' symbol",
    ),
    pytest.param(
        {
            "email": "email@mailboxcom",
            "expected_error": "Email wrong format. try adding a '.' symbol",
        },
        id="email without '.' symbol",
    ),
    pytest.param(
        {
            "email": "wiitkzpxunlvevrjvvzgipryalytmybnkmqxzhzzttxekoqucb@a.vtp",
            "expected_error": "Must be between 6 and 55 characters",
        },
        id="invalid data (56 characters)",
    ),
    pytest.param(
        {
            "email": " example@box.com",
            "expected_error": "Invalid characters in email",
        },
        id="invalid data (two spaces before)",
    ),
    pytest.param(
        {
            "email": " example@box.com",
            "expected_error": "Invalid characters in email",
        },
        id="invalid data (two spaces between)",
    ),
    pytest.param(
        {
            "email": "example@box.com ",
            "expected_error": "Invalid characters in email",
        },
        id="invalid data (two spaces after)",
    ),
    pytest.param(
        {
            "email": "лучшая@почта.ком",
            "expected_error": "Invalid characters in email",
        },
        id="invalid data (russian letters)",
    ),
    pytest.param(
        {
            "email": "example@MaiButihavefdfsdfsdfsdfsdfsdfsdfsdfsfsdfsdsgsgsdgsdgsdgsdgsdgsdgsdgdgsgsdgsgl.com",
            "expected_error": "Must be between 6 and 55 characters",
        },
        id="invalid_email_too_much_characters",
    ),
]


VALID_PHONES = [
    pytest.param(
        "+359 881234567",
        id="valid_phone_bulgaria_mobile_operator",
    ),
    pytest.param(
        "+48299976714",
        id="valid_existing_phone_with_co_owner_rules",
    ),
]


INVALID_PHONES = [
    pytest.param(
        {
            "phone": "+48123456!!",
            "expected_error": "Phone number must contain only digits",
        },
        id="phone_contains_exclamation_marks",
    ),
    pytest.param(
        {
            "phone": "+48123456-aaa",
            "expected_error": "Phone number must contain only digits",
        },
        id="phone_contains_letters",
    ),
    pytest.param(
        {
            "phone": "+48345678-91",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_10_digits",
    ),
    pytest.param(
        {
            "phone": "+483456789-1234",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_13_digits",
    ),
    pytest.param(
        {
            "phone": "48299976778",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_without_plus",
    ),
    pytest.param(
        {
            "phone": "4+8299976778",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_digits_before_plus",
    ),
    pytest.param(
        {
            "phone": "+995 976778",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_georgian_code",
    ),
    pytest.param(
        {
            "phone": "+48 54789654789654122",
            "expected_error": "Phone number wrong format",
        },
        id="phone_too_many_digits",
    ),
    pytest.param(
        {
            "phone": "+485752",
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="phone_6_digits",
    ),
    pytest.param(
        {
            "phone": "+48299976714",
            "expected_error": "User account with this phone number already exists. Enter another phone number or log in",
        },
        id="already_registered_phone_number",
    ),
    pytest.param(
        {
            "phone": "+32 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_belgium_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+33 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_france_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+49 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_germany_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+39 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_italy_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+48 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_poland_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+34 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_spain_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+46 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_sweden_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+44 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_uk_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+420 999999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_czech_republic_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+359 29 9999999",
            "expected_error": "Phone number wrong format",
        },
        id="phone_bulgaria_world_code_without_mobile_operator",
    ),
    pytest.param(
        {
            "phone": "+32 50 5487565",
            "expected_error": "Phone number wrong format",
        },
        id="phone_belgium_landline_code",
    ),
    pytest.param(
        {
            "phone": "+39 06 5487565",
            "expected_error": "Phone number wrong format",
        },
        id="phone_italy_landline_code",
    ),
    pytest.param(
        {
            "phone": "+34 91 5487565",
            "expected_error": "Phone number wrong format",
        },
        id="phone_spain_landline_code",
    ),
    pytest.param(
        {
            "phone": "+46 4 548756",
            "expected_error": "Phone number wrong format",
        },
        id="phone_sweden_landline_code",
    ),
    pytest.param(
        {
            "phone": "+359 32 5487565",
            "expected_error": "Phone number wrong format",
        },
        id="phone_bulgaria_landline_code",
    ),
]
