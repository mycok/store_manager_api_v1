import json

from tests.fixture import TestFixture


class TestFetchSingleSale(TestFixture):
    """
    Test fetch single sale object
    """
    def test_get_sale_by_id(self):
        # Test successful GET request to fetch a sale by id
        with self.client:
            # post a product
            _ = self.create_product()
            # post a sale
            response = self.create_sale()
            data = json.loads(response.data.decode())
            sale_id = data['sale_id']

            # get sale by id
            response = self.client.get(
                '/api/v1/sales/{}'.format(sale_id),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

    def test_cant_fetch_a_sale_an_with_out_of_range_index(self):
        """
        Test unsuccessful GET request to fetch
        a sale with an out of range id index
        """
        with self.client:
            # post a product
            _ = self.create_product()
            # post a sale
            _ = self.create_sale()
            # get that sale by id
            response = self.client.get(
                '/api/v1/sales/10',
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'unsuccessful')
            self.assertEqual(
                data['message'],
                'sale record with ID 10 doesnot exist')
