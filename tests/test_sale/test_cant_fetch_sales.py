import json
from tests.fixture import TestFixture


class TestCantFetchAllSales(TestFixture):
    """
    """
    def test_get_all_sales_from_an_empty_dict(self):
        """
        Test unsuccessful GET request to
        fetch all sales from an empty dictionary
        """
        with self.client:
            response = self.get_all_sales()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'No sales records available')
