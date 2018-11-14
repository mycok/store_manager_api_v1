import json
from tests.fixture import TestFixture


class TestCreateProduct(TestFixture):

    def test_create_a_product(self):
        # Test successful POST request to create a product
        with self.client:
            response = self.create_product()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'macbookair has been added')

    def test_create_a_product_with_attendant_previllages(self):
        # Test unsuccessful POST request to create a product
        with self.client:
            response = self.cant_create_product_as_an_attendant()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'], 'Admin previllages required')

    def test_cant_create_a_duplicate_product(self):
        # Test unsuccessful POST request to create a duplicate product
        with self.client:
            _ = self.create_product()

            new_response = self.create_product()
            data = json.loads(new_response.data.decode())
            self.assertEqual(new_response.status_code, 400)
            self.assertEqual(data['message'], 'product macbookair already exists')

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
        create a product with an empty name string
        """
        with self.client:
            response = self.create_product_with_an_empty_string()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product name should contain atleast three characters, and no numbers')
            self.assertEqual(data['status'], 'unsuccessful')
