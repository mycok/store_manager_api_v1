import json

from tests.fixture import FixtureTest


class TestFetchAllProducts(FixtureTest):
    def test_get_all_products(self):
        """
        Test successful GET request to
        fetch all products
        """
        with self.client:
            # create a product
            _ = self.create_product()

            # get all products
            get_response = self.get_all_products()

            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIsInstance(data['products'], list)
            self.assertEqual(data['status'], 'successful')
            self.assertTrue(data['products'][0]['name'], 'macbook air')

    def test_try_to_get_all_products_from_an_empty_dict(self):
        """
        Test unsuccessful GET request to
        fetch all products from an empty dictionary
        """
        with self.client:
            response = self.get_all_products()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'No products available')
