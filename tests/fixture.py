from unittest import TestCase
import json

from flasky import create_app
from flasky.config import TestingConfig
from flasky.product.product_model import Product
from flasky.sale.sale_model import Sale
from flasky.product.product_controller import controller
from flasky.database.postgres import DataBase as db


class TestFixture(TestCase):
    """
    Test class template for test re-usable objects
    """

    def setUp(self):
        self.app = create_app(config_name=TestingConfig)
        self.client = self.app.test_client()
        self.db = db()
        self.db.connect('test_database', 'Myko', 1987)
        self.db.create_db_tables()
        self.product = Product('macbook', 'computers/laptops', 3, 1499.0)
        self.sale = Sale('kibuuka')

    def tearDown(self):
        self.db.drop_tables()
        self.db.close()
        controller.products.clear()

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

# sale helper methods
    def create_sale(self):
        """
        send a POST request to create a sale object
        """
        return self.client.post(
            '/api/v1/sales', content_type='application/json',
            data=json.dumps(
                dict(attendant='michael')))

    def create_sale_without_the_attendant_attribute(self):
        """
        send a POST request to create a sale object
        with  a missing required parameter.
        """
        return self.client.post(
            '/api/v1/sales', content_type='application/json',
            data=json.dumps(dict(attendant='  ')))

    def get_all_sales(self):
        """
        send a GET request to fetch all sales
        """
        return self.client.get(
             '/api/v1/sales', content_type='application/json')

# shopping cart helper methods
    def add_product_to_shopping_cart(self):
        """
        send a POST request to add a product to cart
        """
        return self.client.post(
           '/api/v1/shopping_cart', content_type='application/json',
           data=json.dumps(dict(name='macbook air', quantity=4))
        )
