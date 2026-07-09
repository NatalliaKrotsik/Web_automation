VALID_SIGN_IN_DATA = [
    {
        "name": "valid_sign_in",
        "email": "dehihal910@fisedo.com",
        "password": "Test123!",
        "expected_status": 200,
    },
]

INVALID_SIGN_IN_DATA = [
    {
        "name": "invalid_email",
        "email": "an@kowalski.test@mailinator.com",
        "password": "Test@1234!",
        "expected_error": "",
        "expected_status": 400,
    },
    {
        "name": "wrong_password",
        "email": "dehihal910@fisedo.com",
        "password": "Tesy778!",
        "expected_error": "Incorrect email or password",
        "expected_status": 401,
    },
    {
        "name": "minim_length",
        "email": "T@g.m",
        "password": "TempP@ss123",
        "expected_error": "Must be between 6 and 55 characters",
        "expected_status": 400,
    },
    {
        "name": "maximum_length",
        "email": "maksmakmakmmmaksmakmakmmaksiki100aksiki100siki100siki100iki100maksmakmakmmaksiki100aksiki100siki100siki100iki100aksiki100aksiki100siki100siki100iki100@gmail.com",
        "password": "TempP@ss123",
        "expected_error": "Must be between 6 and 55 characters",
        "expected_status": 400,
    },
    {
        "name": "invalid_format_email",
        "email": "dehihal910fisedo.com",
        "password": "Test123!",
        "expected_error": "",
        "expected_status": 400,
    },
]
