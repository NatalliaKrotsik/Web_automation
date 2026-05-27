import pytest

VALID_PAYLOAD = {
    "email": "alina.petrova@gmail.com",
    "phone": "+359881234567",
}
VALID_EMAILS = [
    pytest.param(
        {
            "email": "alina.petrova@gmail.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_with_dot",
    ),
    pytest.param(
        {
            "email": "alina_petrova@gmail.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_with_underscore",
    ),
    pytest.param(
        {
            "email": "alina-petrova@gmail.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_with_dash",
    ),
    pytest.param(
        {
            "email": "prettyExample@box.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email",
    ),
    pytest.param(
        {
            "email": "prettyExample@box.by",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_by",
    ),
    pytest.param(
        {
            "email": "prettyExample@box.ru",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_ru",
    ),
    pytest.param(
        {
            "email": "prettyExample@box.LOL",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_lol",
    ),
    pytest.param(
        {
            "email": "m@k.by",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_lower_limit",
    ),
    pytest.param(
        {
            "email": "mr@k.by",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_seven_ch",
    ),
    pytest.param(
        {
            "email": "wiitzpxunlvevrjvvzgipryalytmbnkmqxzhzztxekoqucb@a.vtp",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_upper_limit",
    ),
    pytest.param(
        {
            "email": "PRETTYEXAMPLE@BOX.COM",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_upper_case",
    ),
    pytest.param(
        {
            "email": "prettyexample@box.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_lower_case",
    ),
    pytest.param(
        {
            "email": "pRettyExaMple@box.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_mix_case",
    ),
]


INVALID_EMAILS = [
    pytest.param(
        {
            "email": "alina!@gmail.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Email wrong format",
        },
        id="invalid_email_exclamation_mark",
    ),
    pytest.param(
        {
            "email": "ali?na@gmail.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Email wrong format",
        },
        id="invalid_email_question_mark",
    ),
    pytest.param(
        {
            "email": r"alina\petrova@gmail.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Email wrong format",
        },
        id="invalid_email_slash",
    ),
    pytest.param(
        {
            "email": "email2mailbox.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Email wrong format. try adding a '@' symbol",
        },
        id="invalid_email_without_at_sign",
    ),
    pytest.param(
        {
            "email": "email@mailboxcom",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Email wrong format. try adding a '.' symbol",
        },
        id="invalid_email_without_dot",
    ),
    pytest.param(
        {
            "email": "wiitkzpxfunlvevrjvvzgipryalytmybnkmqxzhzzttxekoqucb@a.vtp",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Must be between 6 and 55 characters",
        },
        id="invalid_email_more_than_upper_limit",
    ),
    pytest.param(
        {
            "email": " prettyExample@box.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Invalid characters in email",
        },
        id="invalid_email_two_spaces_before",
    ),
    pytest.param(
        {
            "email": "prettyE xample@box.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Invalid characters in email",
        },
        id="invalid_email_spaces_between",
    ),
    pytest.param(
        {
            "email": "prettyExample@box.com ",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Invalid characters in email",
        },
        id="invalid_email_two_spaces_after",
    ),
    pytest.param(
        {
            "email": "лучшая@почта.ком",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Invalid characters in email",
        },
        id="invalid_email_russian",
    ),
    pytest.param(
        {
            "email": "pretty@MaiButihavefdfsdfsdfsdfsdfsdfsdfsdfsfsdfsdsgsgsdgsdgsdgsdgsdgsdgsdgdgsgsdgsgl.com",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "Must be between 6 and 55 characters",
        },
        id="invalid_email_too_much_characters",
    ),
    pytest.param(
        {
            "email": "",
            "phone": "+48299976714",
            "expected_status": 422,
            "expected_error": "The field cannot be empty",
        },
        id="invalid_email_empty_field",
    ),
    pytest.param(
        {
            "email": "prettyexample@boxer.com",
            "phone": "+48299976714",
            "expected_status": 409,
            "expected_error": "User account with this email already exists. Enter another email or log in",
        },
        id="invalid_email_have_already_exist",
    ),
]


VALID_PHONES = [
    pytest.param(
        {
            "email": "dtest@gmail.com",
            "phone": "+359 881234567",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_bulgaria_operator",
    ),
    pytest.param(
        {
            "email": "test@gmail.com",
            "phone": "+48299976714",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_exist_co_owner_rule",
    ),
    pytest.param(
        {
            "email": "testt@gmail.com",
            "phone": "+48345678-912",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_eleven_char",
    ),
    pytest.param(
        {
            "email": "tesst@gmal.com",
            "phone": "+483456789-123",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_twelve_char",
    ),
    pytest.param(
        {
            "email": "Testtest@gmail.com",
            "phone": "+32 4 70123456",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_belgium",
    ),
    pytest.param(
        {
            "email": "dootest@gmail.com",
            "phone": "+33 6 45678901",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_france",
    ),
    pytest.param(
        {
            "email": "llttest@gmail.com",
            "phone": "+49 015 123456789",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_germany",
    ),
    pytest.param(
        {
            "email": "nnsttest@gmail.com",
            "phone": "+39 333 12345678",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_phone_italy",
    ),
    pytest.param(
        {
            "email": "qqesttest@gmail.com",
            "phone": "+48 500123456",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_poland",
    ),
    pytest.param(
        {
            "email": "rrrsttest@gmail.com",
            "phone": "+34 658 123456",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_spain",
    ),
    pytest.param(
        {
            "email": "Testtffest@gmail.com",
            "phone": "+46 70 1234567",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_sweden",
    ),
    pytest.param(
        {
            "email": "Testetest@gmail.com",
            "phone": "+44 7 701900123",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_uk",
    ),
    pytest.param(
        {
            "email": "Tsttest@gmail.com",
            "phone": "+420 773 123 456",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_czech_republic",
    ),
    pytest.param(
        {
            "email": "Testtoooo@gmail.com",
            "phone": "+359 881234567",
            "expected_status": 201,
            "expected_error": None,
        },
        id="valid_email_bulgaria",
    ),
]


INVALID_PHONES = [
    pytest.param(
        {
            "email": "huhuh@gmail.com",
            "phone": "+48123456!!",
            "expected_status": 422,
            "expected_error": "Phone number must contain only digits",
        },
        id="invalid_phone_exclamation_mark",
    ),
    pytest.param(
        {
            "email": "oioioi@hmail.com",
            "phone": "+48123456-aaa",
            "expected_status": 422,
            "expected_error": "Phone number must contain only digits",
        },
        id="invalid_phone_letter",
    ),
    pytest.param(
        {
            "email": "ianian@gmail@gmail.com",
            "phone": "+48345678-91",
            "expected_status": 422,
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="invalid_phone_ten_characters",
    ),
    pytest.param(
        {
            "email": "youyou@gmail.com",
            "phone": "+483456789-1234",
            "expected_status": 422,
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="invalid_phone_thirteen_characters",
    ),
    pytest.param(
        {
            "email": "gygygy@gmail.com",
            "phone": "48299976778",
            "expected_status": 422,
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="invalid_phone_without_plus_sign",
    ),
    pytest.param(
        {
            "email": "lily@gmail.com",
            "phone": "4+8299976778",
            "expected_status": 422,
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="invalid_phone_digits_before_plus_sign",
    ),
    pytest.param(
        {
            "email": "nunununu@gmail.com",
            "phone": "+7 299976778",
            "expected_status": 422,
            "expected_error": "Phone number length should be at least 11 symbols",
        },
        id="invalid_phone_russian_code",
    ),
    pytest.param(
        {
            "email": "bbbiot@gmail.com",
            "phone": "+48 54789654789654122",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_more_than_allowed_characters",
    ),
    pytest.param(
        {
            "email": "ootyr@gmail.com",
            "phone": "+485752",
            "expected_status": 422,
            "expected_error": None,
        },
        id="invalid_phone_six_characters",
    ),
    pytest.param(
        {
            "email": "piopio@gmail.com",
            "phone": "+48299976714",
            "expected_status": 409,
            "expected_error": "User account with this phone number already exists. Enter another phone number or log in",
        },
        id="invalid_phone_have_already_exist",
    ),
    pytest.param(
        {
            "email": "tytytyt@gmail.com",
            "phone": "+32 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_belgium",
    ),
    pytest.param(
        {
            "email": "momom@gmail.com",
            "phone": "+33 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_france",
    ),
    pytest.param(
        {
            "email": "vbvvbvbbb@gmail.com",
            "phone": "+49 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_germany",
    ),
    pytest.param(
        {
            "email": "xcxcx@gmail.com",
            "phone": "+39 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_italy",
    ),
    pytest.param(
        {
            "email": "ffgfgfg@gmail.com",
            "phone": "+48 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_poland",
    ),
    pytest.param(
        {
            "email": "rerer@gmail.com",
            "phone": "+34 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_spain",
    ),
    pytest.param(
        {
            "email": "njnjnjn@gmail.com",
            "phone": "+46 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_sweden",
    ),
    pytest.param(
        {
            "email": "kjkjkj@gmail.com",
            "phone": "+44 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_uk",
    ),
    pytest.param(
        {
            "email": "bvbnn@gmail.com",
            "phone": "+420 999999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_czech_republic",
    ),
    pytest.param(
        {
            "email": "mkmkmkm@gmail.com",
            "phone": "+359 29 9999999",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_operator_bulgaria",
    ),
    pytest.param(
        {
            "email": "popopo@gmail.com",
            "phone": "+32 50 5487565",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_landline_belgium",
    ),
    pytest.param(
        {
            "email": "asasas@gmail.com",
            "phone": "+39 06 5487565",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_landline_italy",
    ),
    pytest.param(
        {
            "email": "ioioiioi@gmail.com",
            "phone": "+34 91 5487565",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_landline_spain",
    ),
    pytest.param(
        {
            "email": "sweden@gmail.com",
            "phone": "+46 4 548756",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_landline_sweden",
    ),
    pytest.param(
        {
            "email": "bgla@gmail.com",
            "phone": "+359 32 5487565",
            "expected_status": 422,
            "expected_error": "Phone number wrong format",
        },
        id="invalid_phone_without_landline_bulgaria",
    ),
    pytest.param(
        {
            "email": "bgla@gmail.com",
            "phone": "",
            "expected_status": 422,
            "expected_error": None,
        },
        id="invalid_phone_empty_field",
    ),
]
