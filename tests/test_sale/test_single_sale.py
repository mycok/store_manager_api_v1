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

            response = self.user_login()
            data = json.loads(response.data.decode())
            token = data['token']

            # get sale by id
            response = self.client.get(
                '/api/v2/sales/{}'.format(sale_id),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            self.assertEqual(response.status_code, 200)

    def test_cant_fetch_a_sale_with_an_invalid_id(self):
        """
        Test unsuccessful GET request to fetch
        a sale with an invalid id
        """
        with self.client:
            # post a product
            _ = self.create_product()
            # post a sale
            _ = self.create_sale()

            response = self.user_login()
            data = json.loads(response.data.decode())
            token = data['token']

            # get sale by id
            response = self.client.get(
                '/api/v2/sales/123456789',
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['status'], 'unsuccessful')
            self.assertEqual(
                data['message'],
                'sale with ID 123456789 doesnot exist')

    def test_attendant_get_sale_by_id(self):
            # Test successful GET request to fetch a sale by id
        with self.client:
            # post a product
            _ = self.create_product()
            # post a sale
            response = self.create_sale()
            data = json.loads(response.data.decode())
            sale_id = data['sale_id']

            response = self.attendant_login()
            data = json.loads(response.data.decode())
            token = data['token']

            # get sale by id
            response = self.client.get(
                '/api/v2/sales/{}'.format(sale_id),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            self.assertEqual(response.status_code, 401)
