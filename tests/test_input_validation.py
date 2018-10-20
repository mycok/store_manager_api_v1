from tests.fixture import FixtureTest
from flasky.product.input_validation import is_product_input_valid


class TestInputValidation(FixtureTest):
    """
    Test input validation function
    """

    def test_product_input_with_missing_name(self):
        is_valid = is_product_input_valid(
            name=None, category='computers', quantity=6, price=1299.0)
        self.assertEqual(is_valid, 'please provide a valid product name')

    def test_product_input_with_missing_category(self):
        is_valid = is_product_input_valid(
            name='macbook pro', category=None, quantity=6, price=1299.0)
        self.assertEqual(is_valid, 'please provide a valid product category')

    def test_product_input_with_missing_quantity(self):
        is_valid = is_product_input_valid(
            name='macbook pro', category='computers', quantity=None, price=1299.0)
        self.assertEqual(is_valid, 'please provide a valid product quantity')

    def test_product_input_with_missing_price(self):
        is_valid = is_product_input_valid(
            name='macbook pro', category='computers', quantity=9, price=0)
        self.assertEqual(is_valid, 'please provide a valid product price')
