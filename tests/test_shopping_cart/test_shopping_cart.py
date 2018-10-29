import json

from tests.fixture import TestFixture


class TestShoppingCart(TestFixture):
    def test_add_product_to_cart(self):
        # create product
        with self.client:
            _ = self.create_product()
        # add product to shopping cart
            response = self.add_product_to_shopping_cart()
            self.assertEqual(response.status_code, 201)

    def test_cant_add_product_invalid_content_type(self):
        # create product
        with self.client:
            _ = self.create_product()
        # add product to shopping cart
            response = self.client.post(
                '/api/v1/shopping_cart', content_type='xml',
                data=json.dumps(dict(name='macbook air', quantity=4))
            )
            self.assertEqual(response.status_code, 400)

    def test_cant_add_product_invalid_name_attribute(self):
        # create product
        with self.client:
            _ = self.create_product()
        # add product to shopping cart
            response = self.client.post(
                '/api/v1/shopping_cart', content_type='application/json',
                data=json.dumps(dict(name='', quantity=4))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'please provide a valid product name')

    def test_cant_add_product_with_invalid_quantity_attribute(self):
        # create product
        with self.client:
            _ = self.create_product()
        # add product to shopping cart
            response = self.client.post(
                '/api/v1/shopping_cart', content_type='application/json',
                data=json.dumps(dict(name='macbook air', quantity=None))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'please provide a valid product quantity')

    def test_cant_add_non_exixting_product(self):
        # create product
        with self.client:
            # add product to shopping cart
            response = self.client.post(
                '/api/v1/shopping_cart', content_type='application/json',
                data=json.dumps(dict(name='macbook air', quantity=3))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product macbook air doesnot exist')
