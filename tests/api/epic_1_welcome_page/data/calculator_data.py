VALID_CALCULATOR_DATA = [
    {"name": "eur_to_pln_sell_amount", "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 1.00, "get_amount": None},
    {"name": "eur_to_pln_get_amount", "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": None, "get_amount": 100.00},
    {"name": "pln_to_eur_sell_amount", "sell_currency": "PLN", "get_currency": "EUR", "sell_amount": 100.00, "get_amount": None},
    {"name": "pln_to_eur_get_amount", "sell_currency": "PLN", "get_currency": "EUR", "sell_amount": None, "get_amount": 100.00},
    {"name": "eur_to_usd_sell_amount", "sell_currency": "EUR", "get_currency": "USD", "sell_amount": 100.00, "get_amount": None},
    {"name": "eur_to_usd_get_amount", "sell_currency": "EUR", "get_currency": "USD", "sell_amount": None, "get_amount": 100.00},
    {"name": "minimum_sell_amount", "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 0.01, "get_amount": None},
    {"name": "maximum_sell_amount", "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 100000.00, "get_amount": None},
    {"name": "decimal_rounding", "sell_currency": "USD", "get_currency": "PLN", "sell_amount": 10.99, "get_amount": None},
    {"name": "gbp_to_pln", "sell_currency": "GBP", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None},
    {"name": "cny_to_pln", "sell_currency": "CNY", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None},
    {"name": "jpy_to_pln", "sell_currency": "JPY", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None},
    {"name": "chf_to_pln", "sell_currency": "CHF", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None},
]

INVALID_CALCULATOR_DATA = [
    {
        "name": "sell_amount_below_minimum",
        "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 0.00, "get_amount": None,
        "expected_status": 422, "expected_error": "Input should be greater than or equal to 0.01",
    },
    {
        "name": "negative_sell_amount",
        "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": -1.00, "get_amount": None,
        "expected_status": 422, "expected_error": "Input should be greater than or equal to 0.01",
    },
    {
        "name": "sell_amount_above_maximum",
        "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 100001.00, "get_amount": None,
        "expected_status": 422, "expected_error": "Input should be less than or equal to 100000",
    },
    {
        "name": "both_amounts_missing",
        "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": None, "get_amount": None,
        "expected_status": 422, "expected_error": "Either sell_amount or get_amount must be provided",
    },
    {
        "name": "both_amounts_provided",
        "sell_currency": "EUR", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": 200.00,
        "expected_status": 422, "expected_error": "Only one of sell_amount or get_amount must be provided",
    },
    {
        "name": "unavailable_sell_currency",
        "sell_currency": "CAD", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 400, "expected_error": "The exchange rate is not available.",
    },
    {
        "name": "unavailable_get_currency",
        "sell_currency": "EUR", "get_currency": "CAD", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 400, "expected_error": "The exchange rate is not available.",
    },
    {
        "name": "same_currencies",
        "sell_currency": "EUR", "get_currency": "EUR", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 400, "expected_error": "Same currencies are not allowed",
    },
    {
        "name": "empty_sell_currency",
        "sell_currency": "", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 422, "expected_error": "String should have at least 3 characters",
    },
    {
        "name": "null_sell_currency",
        "sell_currency": None, "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 422, "expected_error": "Input should be a valid string",
    },
    {
        "name": "lowercase_sell_currency",
        "sell_currency": "eur", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 400, "expected_error": "The exchange rate is not available.",
    },
    {
        "name": "special_chars_sell_currency",
        "sell_currency": "@@@", "get_currency": "PLN", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 400, "expected_error": "The exchange rate is not available.",
    },
    {
        "name": "empty_get_currency",
        "sell_currency": "EUR", "get_currency": "", "sell_amount": 100.00, "get_amount": None,
        "expected_status": 422, "expected_error": "String should have at least 3 characters",
    },
    {
        "name": "null_get_currency",
        "sell_currency": "EUR", "get_currency": None, "sell_amount": 100.00, "get_amount": None,
        "expected_status": 422, "expected_error": "Input should be a valid string",
    },
]
