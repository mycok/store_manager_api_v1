from tests.fixture import FixtureTest
from flasky.product.manager import product_manager


class TestProductManager(FixtureTest):
    """
    Test class for testing product manager class
    """
    def test_product_manager_init(self):
        self.assertIsInstance(product_manager.products, dict)

    def test_add_new_product_increases_products_count(self):
        product_manager.add_product(self.product)
        self.assertEqual(len(product_manager.products), 1)
