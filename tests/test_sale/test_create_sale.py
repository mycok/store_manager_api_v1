import json

from tests.fixture import TestFixture


class TestCreateSale(TestFixture):
    """

    """
    def test_create_a_sale(self):
        # Test successful POST request to create a sale
        with self.client:
            # add product to cart
            _ = self.add_product_to_cart()
            # then create a sale with the appended product
            response = self.create_sale()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['attendant'], 'michael')

    def test_create_sale_with_wrong_content_type(self):
        """
        Test unsuccessful POST request to
        create a sale with wrong content type
        """
        with self.client:
            response = self.create_sale_with_wrong_content_type()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'request must be of type json')

    def test_create_sale_without_attendant_attribute(self):
        """
        Test unsuccessful POST request to
        create a sale with missing required attribute
        """
        with self.client:
            response = self.create_sale_without_the_attendant_attribute()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'],
                'please provide a valid attendant name')

    def test_cant_create_sale_as_an_admin(self):
        """
        Test unsuccessful POST request to
        create a sale with admin previllages
        """
        with self.client:
            response = self.create_sale_as_admin()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                data['message'],
                'Attendant previllages required')
