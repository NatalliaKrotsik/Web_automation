import requests
import unittest

class TestCardProductsAPI(unittest.TestCase):

    BASE_URL = 'https://api.example.com/card-products'  # Replace with actual API endpoint

    def test_get_card_products(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list, "Response should be a list")

    def test_get_card_product_by_id(self):
        card_id = 1  # Replace with a valid card ID
        response = requests.get(f'{self.BASE_URL}/{card_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json(), "Response should contain 'id'")

    def test_create_card_product(self):
        new_product = {'name': 'New Card', 'type': 'credit'}  # Replace with actual expected fields
        response = requests.post(self.BASE_URL, json=new_product)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json(), "Response should contain 'id'")

    def test_update_card_product(self):
        card_id = 1  # Replace with a valid card ID
        updated_product = {'name': 'Updated Card Name'}  # Replace with actual expected fields
        response = requests.put(f'{self.BASE_URL}/{card_id}', json=updated_product)
        self.assertEqual(response.status_code, 200)

    def test_delete_card_product(self):
        card_id = 1  # Replace with a valid card ID
        response = requests.delete(f'{self.BASE_URL}/{card_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()