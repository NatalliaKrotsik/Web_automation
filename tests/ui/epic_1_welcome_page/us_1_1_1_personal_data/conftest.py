import pytest
import yaml


def _load_data() -> dict:
    with open("tests/ui/epic_1_welcome_page/data/test_personal_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


_DATA = _load_data()


@pytest.fixture(scope="function")
def personal_info_data() -> dict:
    return _DATA