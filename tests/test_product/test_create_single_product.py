import json
from tests.fixture import TestFixture


class TestCreateProduct(TestFixture):

    def test_create_a_product(self):
        # Test successful POST request to create a product
        with self.client:
            response = self.create_product()
            data = json.loads(response.data.decode())
            # self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'macbookair has been added')

    def test_cant_create_a_duplicate_product(self):
        # Test successful POST request to create a product
        with self.client:
            _ = self.create_product()

            new_response = self.create_product()
            data = json.loads(new_response.data.decode())
            self.assertEqual(new_response.status_code, 400)
            self.assertEqual(data['message'], 'product macbookair already exists')

    def test_create_product_with_wrong_content_type(self):
        """
         Test unsuccessful POST request to
        create a product with wrong content type
        """
        with self.client:
            response = self.create_product_with_wrong_content_type()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'request must be of type json')
            self.assertEqual(data['status'], 'unsuccessful')

    def test_create_product_with_a_missing_attribute(self):
        """
        Test unsuccessful POST request to
        create a product with missing required attribute
        """
        with self.client:
            response = self.create_product_with_missing_attributes()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'quantity should be a number greater than zero')
            self.assertEqual(data['status'], 'unsuccessful')

    def test_cant_create_product_with_an_empty_string_as_name(self):
        """
         Test unsuccessful POST request to
        create a product with an empty string
        """
        with self.client:
            response = self.create_product_with_an_empty_string()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product name should contain atleast three characters, and no numbers')
            self.assertEqual(data['status'], 'unsuccessful')
