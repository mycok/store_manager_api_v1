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
            response = self.create_product()
            # self.assertEqual(response.status_code, 201)

            new_response = self.create_product()
            data = json.loads(new_response.data.decode())
            self.assertEqual(new_response.status_code, 400)
            self.assertEqual(data['message'], 'Product macbookair already exists')

    def test_create_product_with_wrong_content_type(self):
        """
         Test unsuccessful POST request to
        create a product with wrong content type
        """
        with self.client:
            response = self.client.post(
                '/api/v1/products',
                content_type="xml",
                data=json.dumps(dict(name='macbook air',
                                category='computers/laptops',
                                quantity=4, price=1499.0)))
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

    def test_cant_create_product_with_an_empty_string(self):
        """
         Test unsuccessful POST request to
        create a product with an empty string
        """
        with self.client:
            response = self.client.post(
                '/api/v1/products',
                content_type="application/json",
                data=json.dumps(dict(name='  ',
                                category='computers/laptops',
                                quantity=4, price=1499.0)))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'product name should contain atleast three characters, and no numbers')
            self.assertEqual(data['status'], 'unsuccessful')
