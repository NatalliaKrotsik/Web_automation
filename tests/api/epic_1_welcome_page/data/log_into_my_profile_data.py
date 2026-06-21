VALID_SIGN_IN_DATA = [
    {
        "name": "valid_sign_in",
        "email": "jan.kowalski.test@mailinator.com",
        "password": "Test@1234!",
        "expected_status": 200,
    },
]

INVALID_SIGN_IN_DATA = [
    {
        "name": "invalid_email",
        "email": "an.kowalski.test@mailinator.com",
        "password": "Test@1234!",
        "expected_error": "Incorrect email or password",
        "expected_status": 400,
    },
    {
        "name": "empty_email",
        "email": "",
        "password": "Test@1234!",
        "expected_error": "",
        "expected_status": 400,
    },
    {
        "name": "email_not_in_system",
        "email": "Tested@gmail.com",
        "password": "TempP@ss123",
        "expected_error": "Incorrect email or password",
        "expected_status": 400,
    },
    {
        "name": "wrong_password",
        "email": "xonib78658@inreur.com",
        "password": "Tesy778!",
        "expected_error": "Incorrect email or password",
        "expected_status": 400,
    },
    {
        "name": "empty_password",
        "email": "xonib78658@inreur.com",
        "password": "",
        "expected_error": "",
        "expected_status": 400,
    },
    {
        "name": "already_logged_in",
        "email": "xonib78658@inreur.com",
        "password": "Aa12345!",
        "expected_error": "",
        "expected_status": 409,
    },
]
