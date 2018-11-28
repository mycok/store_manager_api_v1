import json

from tests.fixture import TestFixture


class TestFetchSingleProduct(TestFixture):
    def test_cant_fetch_product_with_out_of_range_index(self):
        """
        Test unsuccessful GET request to fetch
         a product with an out of range id index
        """
        with self.client:
            response = self.invalid_fetch_product()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product with ID 3 doesnot exist')

    def test_get_product_by_id(self):
        # Test successful GET request to fetch a product by id
        with self.client:
            # post a product
            response = self.fetch_product()
            self.assertEqual(response.status_code, 200)

    def test_update_product_by_id(self):
        with self.client:
            response = self.update_product()
            self.assertEqual(response.status_code, 200)

    def test_cant_update_product_with_invalid_content_type(self):
        with self.client:
            response = self.cant_update_product_with_invalid_content_type()
            self.assertEqual(response.status_code, 400)

    def test_cant_update_product_as_an_attendant(self):
        with self.client:
            response = self.cant_update_product_as_an_attendant()
            self.assertEqual(response.status_code, 401)
