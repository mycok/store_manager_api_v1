from unittest import TestCase
import json
from flasky import create_app
from flasky.config import TestingConfig
from flasky.product.model import Product


class FixtureTest(TestCase):
    """
    Test class template for test re-usable objects
    """

    def setUp(self):
        self.app = create_app(config_name=TestingConfig)
        self.client = self.app.test_client()
        self.product = Product('macbook air', 'computers/laptops', 3, 1499.0)

    def tearDown(self):
        pass
