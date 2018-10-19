from unittest import TestCase
import json
from flasky import create_app
from flasky.config import TestingConfig
from flasky.product.model import Product
from flasky.product.manager import product_manager


class FixtureTest(TestCase):
    """
    Test class template for test re-usable objects
    """

    def setUp(self):
        self.app = create_app(config_name=TestingConfig)
        self.client = self.app.test_client()
        self.product = Product('macbook air', 'computers/laptops', 3, 1499.0)

    def tearDown(self):
        product_manager.products.clear()

    # Product Model helper methods
    def create_product(self):
        """
        send a POST request to create a product object
        """
        return self.client.post(
            '/api/v1/products', content_type='application/json',
            data=json.dumps(dict(name='macbook air',
                            category='computers/laptops',
                            quantity=4, price=1499.0)))

    def create_product_with_missing_attributes(self):
        """
        send a POST request to create a product object
        with missing required parameters.
        """
        return self.client.post(
            '/api/v1/products', content_type='application/json',
            data=json.dumps(dict(name='macbook air',
                            category='computers/laptops',
                            price=1499.0)))

    def get_all_products(self):
        """
        send a GET request to fetch all products
        """
        return self.client.get(
             '/api/v1/products', content_type='application/json')
