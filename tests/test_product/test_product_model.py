from tests.fixture import FixtureTest


class TestProductModel(FixtureTest):
    """
    Test class for testing product initialisation
    """

    def test_product_init(self):
        self.assertEqual(self.product.name, 'macbook')
        self.assertEqual(self.product.category, 'computers/laptops')
        self.assertEqual(self.product.price, 1499.0)

    def test_convert_product_to_json(self):
        dict_product = self.product.to_json()
        self.assertIsInstance(dict_product, dict)
