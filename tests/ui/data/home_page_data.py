import pytest

NAV_ITEMS = [
    pytest.param("Cards", id="cards_nav"),
    pytest.param("Accounts", id="accounts_nav"),
    pytest.param("Deposits", id="deposits_nav"),
    pytest.param("Loans", id="loans_nav"),
    pytest.param("Exchange rates", id="exchange_rates_nav"),
    pytest.param("ATMs", id="atms_nav"),
]
