import pytest

VALID_SIGN_IN_DATA = [
    pytest.param("jan.kowalski.test@mailinator.com", "Test@1234!", 200, id="Valid sign in data"),
]
INVALID_SIGN_IN_DATA = [
    pytest.param(
        "an.kowalski.test@mailinator.com", "Test@1234!", "Incorrect email or password", 400, id="Invalid email"
    ),
    pytest.param("", "Test@1234!", "", 400, id="Empty email"),
    pytest.param(
        "Tested@gmail.com", "TempP@ss123", "Incorrect email or password", 400, id="Email doesnt exist in the system"
    ),
    pytest.param("xonib78658@inreur.com", "Tesy778!", "Incorrect email or password", 400, id="Wrong password"),
    pytest.param("xonib78658@inreur.com", "", "", 400, id="empty password"),
    pytest.param("xonib78658@inreur.com", "Aa12345!", "", 409, id="has already logged in"),
]
