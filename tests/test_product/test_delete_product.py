import json

from tests.fixture import TestFixture


class TestDeleteSingleProduct(TestFixture):
    def test_delete_product_by_id(self):
        with self.client:
            response = self.delete_product()
            self.assertEqual(response.status_code, 200)

    def test_cant_delete_product_with_invalid_content_type(self):
        with self.client:
            response = self.cant_delete_product_with_invalid_content_type()
            self.assertEqual(response.status_code, 400)

    def test_cant_delete_product_as_an_attendant(self):
        with self.client:
            response = self.cant_delete_product_as_an_attendant()
            self.assertEqual(response.status_code, 401)
