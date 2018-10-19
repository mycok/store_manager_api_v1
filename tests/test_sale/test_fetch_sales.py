import json
from tests.fixture import FixtureTest


class TestFetchAllSales(FixtureTest):
    def test_get_all_sales(self):
        """
        Test successful GET request to
        fetch all sales
        """
        with self.client:
            # create a product
            _ = self.create_product()

            # create a sale
            _ = self.create_sale()

            # get all products
            get_response = self.get_all_sales()

            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIsInstance(data['sales'], list)
            self.assertEqual(data['status'], 'successful')
            self.assertEqual(data['sales'][0]['attendant'], 'michael')
