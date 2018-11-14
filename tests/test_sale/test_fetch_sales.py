import json
from tests.fixture import TestFixture


class TestFetchAllSales(TestFixture):
    def test_get_all_sales(self):
        """
        Test successful GET request to
        fetch all sales
        """
        with self.client:
            # create and product to cart
            _ = self.add_product_to_cart()
            # create a sale
            _ = self.create_sale()

            # get all products
            get_response = self.get_all_sales()

            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIsInstance(data['sales'], list)

    def test_attendant_can_fetch_all_her_sales_records(self):
        """
        Test successful GET request to
        fetch all sales by attendant
        """
        with self.client:
            # create and product to cart
            _ = self.add_product_to_cart()
            # create a sale
            response = self.create_sale()
            data = json.loads(response.data.decode())
            attendant_name = data['attendant']

            # get all products
            get_response = self.get_all_sales_for_an_attendant(attendant_name)

            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIsInstance(data['sales'], list)

    def test_cant_fetch_sales_without_a_token(self):
        """
        Test unsuccessful GET request to
        fetch all sales as an attendant
        """
        with self.client:
            response = self.get_all_sales_without_a_token()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'], 'Missing a token')

    def test_cant_fetch_sales_with_attendant_previllages(self):
        """
        Test unsuccessful GET request to
        fetch all sales as an attendant
        """
        with self.client:
            response = self.get_all_sales_as_an_attendant()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'], 'Admin previllages required')
