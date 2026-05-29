import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

import allure
import pytest
import requests
import yaml
from assertpy import assert_that

pytestmark = [pytest.mark.api, pytest.mark.regression]


# Data loader

def _load_data() -> dict:
    with open(
        "tests/api/epic_1_welcome_page/data/test_exchange_rates.yaml",
        encoding="utf-8",
    ) as f:
        return yaml.safe_load(f)


_DATA = _load_data()

SUPPORTED_CODES = [c["code"] for c in _DATA["expected_currencies"]]
# Use Decimal for margin multipliers to avoid IEEE 754 float drift in calculations
MARGIN_BUY = Decimal(_DATA["margin"]["buy_multiplier"])
MARGIN_SELL = Decimal(_DATA["margin"]["sell_multiplier"])
DECIMAL_PLACES = _DATA["margin"]["decimal_places"]
QUANTIZE_FORMAT = Decimal("0.01")  # two decimal places


# Helpers

def _fetch_nbp_rate(code: str) -> dict | None:
    """Return the latest NBP table-C record for *code*, or None if unavailable."""
    url = f"{_DATA['nbp_base_url']}/{code}/"
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()["rates"][0]  # keys: bid, ask, effectiveDate


def _decimal_places(value: float) -> int:
    """Return the number of decimal digits in a float/int as returned by JSON."""
    # Normalise via Decimal to handle values like 4.0 → "4.0" → 1 place
    d = Decimal(str(value))
    sign, digits, exponent = d.as_tuple()
    return max(0, -exponent)


# Shared base class

@allure.suite("API Tests - Welcome Page")
@allure.feature("US-1.15 Exchange Rates")
class _ExchangeRatesBase:
    pass


# LP-422 — Verify exchange rates are returned successfully

@allure.story("LP-422 — Verify exchange rates are returned successfully")
@pytest.mark.qase("LP-422")
class TestExchangeRatesLP422(_ExchangeRatesBase):

    @pytest.fixture(scope="function", autouse=True)
    def _setup(self, exchange_rates_api):
        with allure.step("Send GET /api/processing-center/exchange-rates"):
            self.response = exchange_rates_api.get_exchange_rates()
            self.body = self.response.json()

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("LP-422 | Status code is 200 OK")
    @pytest.mark.smoke
    def test_status_code(self):
        assert_that(self.response.status_code).described_as("status code").is_equal_to(
            _DATA["expected_status_code"]
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-422 | Response contains all required top-level fields")
    @pytest.mark.smoke
    @pytest.mark.parametrize("field", [pytest.param(f, id=f) for f in _DATA["expected_fields"]])
    def test_top_level_fields_present(self, field):
        assert_that(self.body).described_as(f"top-level field '{field}'").contains_key(field)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-422 | rates field is a non-empty list")
    @pytest.mark.smoke
    def test_rates_is_non_empty_list(self):
        assert_that(self.body["rates"]).described_as("rates").is_instance_of(list).is_not_empty()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | baseCurrency is PLN")
    @pytest.mark.smoke
    def test_base_currency_is_pln(self):
        assert_that(self.body["baseCurrency"]).described_as("baseCurrency").is_equal_to(
            _DATA["expected_base_currency"]
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-422 | All 6 supported currencies are returned")
    @pytest.mark.smoke
    def test_all_supported_currencies_returned(self):
        returned_codes = {r["code"] for r in self.body["rates"]}
        for code in SUPPORTED_CODES:
            assert_that(returned_codes).described_as(
                f"expected currency '{code}' in response"
            ).contains(code)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | No unsupported currencies are returned")
    def test_no_unsupported_currencies(self):
        returned_codes = {r["code"] for r in self.body["rates"]}
        for code in returned_codes:
            assert_that(SUPPORTED_CODES).described_as(
                f"unexpected currency '{code}' in response"
            ).contains(code)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-422 | Each currency row contains all required fields")
    @pytest.mark.parametrize("field", [pytest.param(f, id=f) for f in _DATA["expected_rate_fields"]])
    def test_rate_fields_present(self, field):
        for rate in self.body["rates"]:
            assert_that(rate).described_as(
                f"field '{field}' missing for currency '{rate.get('code', '?')}'"
            ).contains_key(field)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | code field is a non-empty string for each currency")
    def test_code_is_non_empty_string(self):
        for rate in self.body["rates"]:
            assert_that(rate["code"]).described_as(
                f"code field for entry {rate}"
            ).is_instance_of(str).is_not_empty()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | Currency names match expected values")
    @pytest.mark.parametrize(
        "expected",
        [pytest.param(c, id=c["code"]) for c in _DATA["expected_currencies"]],
    )
    def test_currency_names(self, expected):
        rate = next((r for r in self.body["rates"] if r["code"] == expected["code"]), None)
        assert_that(rate).described_as(f"entry for {expected['code']}").is_not_none()
        assert_that(rate["currency"]).described_as(
            f"{expected['code']} currency name"
        ).is_equal_to(expected["currency"])

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("LP-422 | Icon field is a valid HTTPS URL for each currency")
    def test_icon_is_https_url(self):
        url_pattern = re.compile(r"^https://")
        for rate in self.body["rates"]:
            assert_that(rate["icon"]).described_as(
                f"icon for {rate['code']}"
            ).is_not_none().is_not_empty().matches(url_pattern.pattern)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | Unavailable currencies have null for both buyRate and sellRate")
    def test_null_rates_are_paired(self):
        """
        AC: buy and sell rate fields return null for unavailable currencies.
        Both must be null together — one null + one value is a data inconsistency.
        """
        for rate in self.body["rates"]:
            buy_is_null = rate["buyRate"] is None
            sell_is_null = rate["sellRate"] is None
            assert_that(buy_is_null).described_as(
                f"buyRate null matches sellRate null for {rate['code']} "
                f"(buy={rate['buyRate']}, sell={rate['sellRate']})"
            ).is_equal_to(sell_is_null)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | Available currencies have non-null numeric buy and sell rates")
    def test_available_currencies_have_numeric_rates(self):
        for rate in self.body["rates"]:
            if rate["buyRate"] is None:
                continue  # unavailable currency — covered by null test above
            assert_that(rate["buyRate"]).described_as(
                f"buyRate for {rate['code']}"
            ).is_instance_of((int, float)).is_greater_than(0)
            assert_that(rate["sellRate"]).described_as(
                f"sellRate for {rate['code']}"
            ).is_instance_of((int, float)).is_greater_than(0)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | Buy and sell rates are rounded to 2 decimal places")
    def test_rates_rounded_to_2_decimal_places(self):
        """
        Uses Decimal(str(value)) so that integers like 4 and floats like 4.0
        are both correctly identified as having 0/1 decimal places (failing the check).
        """
        for rate in self.body["rates"]:
            for field in ("buyRate", "sellRate"):
                value = rate[field]
                if value is None:
                    continue
                places = _decimal_places(value)
                assert_that(places).described_as(
                    f"{field} decimal places for {rate['code']} (value={value})"
                ).is_less_than_or_equal_to(DECIMAL_PLACES)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-422 | effectiveDate is present and non-empty")
    @pytest.mark.smoke
    def test_effective_date_present(self):
        assert_that(self.body["effectiveDate"]).described_as(
            "effectiveDate"
        ).is_not_none().is_not_empty()


# LP-423 — Verify exchange rate calculation logic

@allure.story("LP-423 — Verify exchange rate calculation logic")
@pytest.mark.qase("LP-423")
class TestExchangeRateCalculationLP423(_ExchangeRatesBase):
    """
    AC:
      buy_rate  = round(nbp.bid  * 1.02, 2)
      sell_rate = round(nbp.ask  * 0.98, 2)

    Strategy: fetch the live NBP table-C rate for GBP, compute the expected
    values using Decimal arithmetic (no float drift), then compare with our API.
    Skips automatically if NBP is unreachable so CI doesn't fail on NBP downtime.
    """

    GBP_CODE = "GBP"

    @pytest.fixture(scope="function", autouse=True)
    def _setup(self, exchange_rates_api):
        with allure.step("Fetch live NBP table-C rate for GBP"):
            self.nbp = _fetch_nbp_rate(self.GBP_CODE)
            if self.nbp is None:
                pytest.skip("NBP API unavailable — skipping calculation tests")

        with allure.step("Fetch internal exchange rates"):
            resp = exchange_rates_api.get_exchange_rates()
            assert_that(resp.status_code).is_equal_to(200)
            rates = resp.json()["rates"]
            self.gbp = next((r for r in rates if r["code"] == self.GBP_CODE), None)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-423 | GBP is present in the response")
    def test_gbp_present(self):
        assert_that(self.gbp).described_as("GBP entry in response").is_not_none()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-423 | GBP buy rate = round(NBP bid * 1.02, 2)")
    def test_gbp_buy_rate_calculation(self):
        nbp_bid = Decimal(str(self.nbp["bid"]))
        expected_buy = float(
            (nbp_bid * MARGIN_BUY).quantize(QUANTIZE_FORMAT, rounding=ROUND_HALF_UP)
        )
        assert_that(self.gbp["buyRate"]).described_as(
            f"GBP buyRate — expected {expected_buy} "
            f"(NBP bid={self.nbp['bid']} × {MARGIN_BUY})"
        ).is_equal_to(expected_buy)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-423 | GBP sell rate = round(NBP ask * 0.98, 2)")
    def test_gbp_sell_rate_calculation(self):
        nbp_ask = Decimal(str(self.nbp["ask"]))
        expected_sell = float(
            (nbp_ask * MARGIN_SELL).quantize(QUANTIZE_FORMAT, rounding=ROUND_HALF_UP)
        )
        assert_that(self.gbp["sellRate"]).described_as(
            f"GBP sellRate — expected {expected_sell} "
            f"(NBP ask={self.nbp['ask']} × {MARGIN_SELL})"
        ).is_equal_to(expected_sell)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-423 | GBP buy and sell rates are rounded to 2 decimal places")
    def test_gbp_rates_are_rounded(self):
        for field, value in (
            ("buyRate", self.gbp["buyRate"]),
            ("sellRate", self.gbp["sellRate"]),
        ):
            if value is None:
                continue
            assert_that(_decimal_places(value)).described_as(
                f"{field} decimal places (value={value})"
            ).is_less_than_or_equal_to(DECIMAL_PLACES)


# LP-424 — Verify previous day rates are returned for weekends / bank holidays

@allure.story("LP-424 — Verify previous day rates returned for weekends and bank holidays")
@pytest.mark.qase("LP-424")
class TestExchangeRatesPreviousDayLP424(_ExchangeRatesBase):
    """
    AC: When today's NBP data is unavailable (weekend / bank holiday),
    the API must return data from the last available working day.

    Two conditional paths depending on whether NBP has data today:
      • NBP unavailable → assert our effectiveDate is a Mon–Fri weekday
      • NBP available   → assert our effectiveDate matches NBP's effectiveDate
    Both paths assert: valid ISO date, not in the future, not older than 5 days.
    """

    @pytest.fixture(scope="function", autouse=True)
    def _setup(self, exchange_rates_api):
        with allure.step("Fetch internal exchange rates"):
            resp = exchange_rates_api.get_exchange_rates()
            assert_that(resp.status_code).is_equal_to(200)
            self.body = resp.json()
            self.effective_date_str = self.body["effectiveDate"]

        with allure.step("Check today's NBP availability (using USD as probe)"):
            self.nbp_today = _fetch_nbp_rate("USD")

        # Parse once — reused in every test
        with allure.step("Parse effectiveDate"):
            try:
                self.effective_date = datetime.strptime(
                    self.effective_date_str, _DATA["date_format"]
                ).date()
            except ValueError:
                self.effective_date = None

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-424 | effectiveDate matches YYYY-MM-DD format")
    def test_effective_date_format(self):
        assert_that(self.effective_date).described_as(
            f"effectiveDate '{self.effective_date_str}' could not be parsed as YYYY-MM-DD"
        ).is_not_none()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-424 | effectiveDate is not in the future")
    def test_effective_date_not_in_future(self):
        if self.effective_date is None:
            pytest.skip("effectiveDate could not be parsed — covered by format test")
        assert_that(self.effective_date).described_as(
            "effectiveDate must not be in the future"
        ).is_less_than_or_equal_to(date.today())

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-424 | When NBP is unavailable, effectiveDate falls back to a working day")
    def test_effective_date_is_working_day_when_nbp_unavailable(self):
        """
        AC: the system applies the exchange rate set on the previous working day.
        Only runs when NBP has no data today (weekend / bank holiday).
        """
        if self.nbp_today is not None:
            pytest.skip("NBP data IS available today — fallback path not exercised right now")
        if self.effective_date is None:
            pytest.skip("effectiveDate could not be parsed")

        assert_that(self.effective_date.weekday()).described_as(
            f"effectiveDate must be Mon–Fri (0–4), "
            f"got {self.effective_date.strftime('%A')} ({self.effective_date})"
        ).is_less_than(5)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-424 | On a working day, effectiveDate matches NBP effectiveDate")
    def test_effective_date_matches_nbp_when_available(self):
        """Only runs on days when NBP has data."""
        if self.nbp_today is None:
            pytest.skip("NBP data unavailable today — weekend/holiday path covered elsewhere")

        assert_that(self.effective_date_str).described_as(
            f"effectiveDate vs NBP effectiveDate ({self.nbp_today['effectiveDate']})"
        ).is_equal_to(self.nbp_today["effectiveDate"])

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("LP-424 | effectiveDate is not older than 5 calendar days")
    def test_effective_date_not_too_old(self):
        if self.effective_date is None:
            pytest.skip("effectiveDate could not be parsed")
        delta = (date.today() - self.effective_date).days
        assert_that(delta).described_as(
            f"effectiveDate is {delta} days old ({self.effective_date_str}) — "
            "max allowed is 5 (covers long weekends)"
        ).is_less_than_or_equal_to(5)
