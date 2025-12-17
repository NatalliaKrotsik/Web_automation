import allure
import pytest
from framework.api.loans_api import LoansAPI
from framework.utils.allure_reporter import make_allure_testcase

@pytest.mark.api
@allure.suite("Epic 1, User Story 1.2: Banks's products and services.")
class TestBanksProductsAndServices:
    @allure.testcase(make_allure_testcase("C7223280"))
    def test_check_the_loans_list(self, get_tokens):
        loans_api = LoansAPI(get_tokens.get("id_token"))
        loans = loans_api.get_all_loans_of_user()
        assert loans.status_code == 200