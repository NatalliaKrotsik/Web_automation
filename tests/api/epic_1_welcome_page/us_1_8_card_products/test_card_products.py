import allure
import pytest
from assertpy import assert_that

pytestmark = [pytest.mark.api, pytest.mark.regression]


@allure.parent_suite("API Tests")
@allure.suite("Welcome Page")
@allure.sub_suite("US-1.8 Card Products")
class _CardProductsBase:
    """Shared Allure hierarchy for all card products API test classes."""


@allure.story("Card products endpoint")
@pytest.mark.qase("LP-370")
class TestCardProductsLP370(_CardProductsBase):

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("LP-370 | Status code is 200 OK")
    def test_status_code(self, card_products_api):
        with allure.step("GET card products"):
            response = card_products_api.get_card_products()
        with allure.step("Assert status code is 200"):
            assert_that(response.status_code).described_as(
                "Card products endpoint must return 200 OK"
            ).is_equal_to(200)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("LP-370 | Response contains non-empty list of cards")
    def test_card_list(self, card_products_api):
        with allure.step("GET card products"):
            response = card_products_api.get_card_products()
        with allure.step("Assert response contains non-empty cards list"):
            body = response.json()
            assert_that(body["cards"]).described_as(
                "Response must contain a non-empty 'cards' list"
            ).is_instance_of(list).is_not_empty()
