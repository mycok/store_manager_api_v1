from tests.fixture import FixtureTest
from flasky.product.product_controller import controller


class TestProductManager(FixtureTest):
    """
    Test class for testing product manager class
    """
    def test_product_manager_init(self):
        self.assertIsInstance(controller.products, dict)

    def test_add_new_product_increases_products_count(self):
        controller.add_product(self.product)
        self.assertEqual(len(controller.products), 1)
