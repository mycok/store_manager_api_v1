import json

from tests.fixture import FixtureTest


class TestFetchSingleProduct(FixtureTest):
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
