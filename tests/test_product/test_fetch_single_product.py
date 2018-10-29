import json

from tests.fixture import TestFixture


class TestFetchSingleProduct(TestFixture):
    def test_cant_fetch_product_with_out_of_range_index(self):
        """
        Test unsuccessful GET request to fetch
         a product with an out of range id index
        """
        with self.client:
            # post a question
            _ = self.create_product()

            # get that question by id
            response = self.client.get(
                '/api/v1/products/3',
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product with ID 3 doesnot exist')

    def test_get_product_by_id(self):
        # Test successful GET request to fetch a product by id
        with self.client:
            # post a product
            post_response = self.create_product()
            post_data = json.loads(post_response.data.decode())
            product_id = post_data.get('product_id')
            self.assertIsInstance(product_id, int)

            # get product by id
            response = self.client.get(
                '/api/v1/products/{}'.format(product_id),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['name'], 'macbook pro')
