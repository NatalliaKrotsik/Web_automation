VALID_SIGN_IN_DATA = [
    {
        "name": "valid_sign_in",
        "email": "dehihal910@fisedo.com",
        "password": "Test123!",
    },
]

INVALID_SIGN_IN_DATA = [
    {
        "name": "invalid_email",
        "email": "an.kowalski.test@mailinator.com",
        "password": "Test@1234!",
        "expected_error": "Incorrect email or password",
    },
    {
        "name": "email_not_in_system",
        "email": "Tested@gmail.com",
        "password": "TempP@ss123",
        "expected_error": "Incorrect email or password",
    },
    {
        "name": "wrong_password",
        "email": "xonib78658@inreur.com",
        "password": "Tesy778!",
        "expected_error": "Incorrect email or password",
    },
]

VALIDATION_SIGN_IN_DATA = [
    {
        "name": "email_without_at_symbol",
        "email": "xonib78658inreur.com",
        "password": "Aa12345!",
        "expected_error": "Email wrong format. Try adding a '@' symbol",
    },
    {
        "name": "email_with_leading_space",
        "email": " xonib78658@inreur.com",
        "password": "Aa12345!",
        "expected_error": "Email address must not contain spaces",
    },
    {
        "name": "email_with_trailing_space",
        "email": "xonib78658@inreur.com ",
        "password": "Aa12345!",
        "expected_error": "Email address must not contain spaces",
    },
]
