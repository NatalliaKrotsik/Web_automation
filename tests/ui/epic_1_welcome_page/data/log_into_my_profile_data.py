import pytest

VALID_SIGN_IN_DATA = [
    pytest.param(
        "jan.kowalski.test@mailinator.com",
        "Test@1234!",
        id="Valid sign in data",
    ),
]
INVALID_SIGN_IN_DATA = [
    pytest.param(
        "an.kowalski.test@mailinator.com",
        "Test@1234!",
        "Incorrect email or password",
        id="Invalid email",
    ),
    pytest.param(
        "Tested@gmail.com",
        "TempP@ss123",
        "Email doesn't exist. Please check and try again",
        id="Email doesn't exist in the system",
    ),
    pytest.param(
        "xonib78658@inreur.com",
        "Tesy778!",
        "Incorrect email or password",
        id="Wrong password",
    ),
]
VALIDATION_SIGN_IN_DATA = [
    pytest.param(
        "xonib78658inreur.com",
        "Aa12345!",
        "Email wrong format. Try adding a '@' symbol",
        id="Email without @ symbol",
    ),
    pytest.param(
        " xonib78658@inreur.com",
        "Aa12345!",
        "Email address must not contain spaces",
        id="Email with space before",
    ),
    pytest.param(
        "xonib78658@inreur.com ",
        "Aa12345!",
        "Email address must not contain spaces",
        id="Email with space after",
    ),
]
