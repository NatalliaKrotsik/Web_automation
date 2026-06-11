import pytest
import yaml

from framework.api.address_api import AddressAPI
from framework.api.exchange_rates_api import ExchangeRatesAPI
from framework.api.personal_data_api import PersonalDataAPI


def _load_baseline() -> dict:
    with open("tests/api/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["valid_baseline"]


_BASELINE = _load_baseline()


@pytest.fixture(scope="function")
def api() -> PersonalDataAPI:
    return PersonalDataAPI()


@pytest.fixture(scope="function")
def exchange_rates_api() -> ExchangeRatesAPI:
    return ExchangeRatesAPI()


@pytest.fixture(scope="function")
def address_api(auth_tokens) -> AddressAPI:
    client = AddressAPI()
    access_token = auth_tokens.get("authenticationResult", {}).get("accessToken")
    client.update_headers({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture(scope="function")
def valid_payload() -> dict:
    return {
        "first_name": _BASELINE["first_name"],
        "middle_name": _BASELINE["middle_name"],
        "last_name": _BASELINE["last_name"],
        "passport_id": _BASELINE["passport_id"],
        "birth_date": _BASELINE["birth_date"],
    }
