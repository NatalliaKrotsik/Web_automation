import allure
import pytest
import yaml
from assertpy import assert_that

pytestmark = [pytest.mark.api, pytest.mark.regression]

def _load_data() -> dict:
    with open(
        "tests/api/epic_1_welcome_page/data/test_card_products.yaml",
        encoding="utf-8",
    ) as f:
        return yaml.safe_load(f)

_DATA = _load_data()
@allure.parent_suite("API Tests")
@allure.suite("API Tests - Welcome Page")
@allure.feature("US-1.8 Card Products")
@pytest.mark.qase("LP-377")
class TestCardProductSlug():
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("LP-377 | Status code is 200 OK")
    @pytest.mark.parametrize("slug",_DATA["slugs"])
    def test_status_code(self, slug, card_products_api):
        response = card_products_api.get_card_product_by_slug(slug)
        assert_that(response.status_code).is_equal_to(_DATA["expected_status_code"])
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("LP-377 | Card returns expected fields")
    @pytest.mark.parametrize("slug",_DATA["slugs"])
    def test_response_fields(self, slug, card_products_api):
        response = card_products_api.get_card_product_by_slug(slug)
        body = response.json()
        for field in _DATA["expected_card_fields"]:
            assert_that(body).contains_key(field)