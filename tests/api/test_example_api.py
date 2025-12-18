import allure
import pytest
from framework.api.loans_api import LoansAPI

@pytest.mark.api
@pytest.mark.qase("US-1.1")
@allure.suite("Example Api Tests")
class TestBanksProductsAndServices:

    @allure.severity(allure.severity_level.NORMAL)
    def test_check_the_loans_list(self, get_tokens):
        loans_api = LoansAPI(get_tokens.get("id_token"))
        loans = loans_api.get_all_loans_of_user()
        assert loans.status_code == 200