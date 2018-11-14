from tests.fixture import TestFixture
from flasky.validator import Validation as v


class TestInputValidation(TestFixture):
    """
    Test input validation function
    """

    def test_product_input_with_missing_name(self):
        is_valid = v.validate_product(
            name=None, category='computers', quantity=6, price=1299.0)
        self.assertEqual(is_valid, 'product name should contain atleast three characters, and no numbers')

    def test_product_input_with_missing_category(self):
        is_valid = v.validate_product(
            name='macbook pro', category=None, quantity=6, price=1299.0)
        self.assertEqual(is_valid, 'product category should contain atleast three characters, and no numbers')

    def test_product_input_with_missing_quantity(self):
        is_valid = v.validate_product(
            name='macbook pro', category='computers', quantity=None, price=1299.0)
        self.assertEqual(is_valid, 'quantity should be a number greater than zero')

    def test_product_input_with_missing_price(self):
        is_valid = v.validate_product(
            name='macbook pro', category='computers', quantity=9, price=0)
        self.assertEqual(is_valid, 'price should be a number greater than zero')

    def test_valid_argument(self):
        self.assertFalse(v.is_valid_length('me'))

    def test_is_arg_string(self):
        self.assertFalse(v.is_arg_string('45'))

    def test_is_valid_number(self):
        self.assertFalse(v.is_valid_numb(0))

    def test_is_valid_currency(self):
        self.assertTrue(v.is_valid_currency(199.0))
