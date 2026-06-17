import allure
import pytest
from assertpy import assert_that

pytestmark = [pytest.mark.api, pytest.mark.regression]

@allure.parent_suite("API Tests")
@allure.suite("API Tests - Welcome Page")
@allure.feature("US-1.8 Card Products")
@pytest.mark.qase("LP-370")
class TestCardProductsLP370:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("LP-370 | Status code is 200 OK")
    def test_status_code(self, card_products_api):
        response = card_products_api.get_card_products()
        assert_that(response.status_code).is_equal_to(200)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-370 | Response contains non-empty list of cards")
    def test_card_list(self, card_products_api):
        response = card_products_api.get_card_products()
        body = response.json()
        assert_that(body["cards"]).is_instance_of(list).is_not_empty()

