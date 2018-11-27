from tests.fixture import TestFixture
import json


class TestFetchAllAttendants(TestFixture):
    def test_admin_cant_successfully_fetch_all_attendants(self):
        with self.client:
            response = self.fetch_all_attendants()
            self.assertEqual(response.status_code, 200)

    def test_admin_can_successfully_fetch_all_attendants(self):
        with self.client:
            response = self.user_login()
            data = json.loads(response.data.decode())
            token = data['token']

            _ = self.create_attendants(token)
            response = self.fetch_all_attendants()
            self.assertEqual(response.status_code, 200)
