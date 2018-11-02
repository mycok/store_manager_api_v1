import json

from tests.fixture import TestFixture


class TestShoppingCart(TestFixture):
    def test_add_product_to_cart(self):
            response = self.add_product_to_shopping_cart()
            self.assertEqual(response.status_code, 201)

    def test_cant_add_product_invalid_content_type(self):
        # add product to shopping cart
            response = self.client.post(
                '/api/v2/cart', content_type='xml',
                data=json.dumps(dict(name='macbook air', quantity=4))
            )
            self.assertEqual(response.status_code, 400)

    def test_cant_add_non_exixting_product(self):
        # create product
        with self.client:
            response = self.client.post(
                '/api/v2/cart', content_type='application/json',
                data=json.dumps(dict(product_id=12345678990, quantity=4)))

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product with ID 12345678990 doesnot exist')
