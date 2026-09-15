import allure
import requests

from framework.api.core.http_client import HttpClient
class CardProductsAPI(HttpClient):
    """Show card products on the welcome page (US-1.8)."""

    def __init__(self):
        super().__init__()
        self.endpoint = "/api/card-products/info"

    @allure.step("Get Card Products")
    def get_card_products(self) -> requests.Response:
        return self.get(path=self.endpoint)
    
    @allure.step("Get Card Products with Slug")
    def get_card_product_by_slug(self, slug: str) -> requests.Response:
        return self.get(path=f"/api/card-products/{slug}")