from tests.fixture import TestFixture
import json


class TestPasswordReset(TestFixture):
    def test_admin_can_successfully_reset_his_password(self):
        with self.client:
            response = self.admin_password_reset()
            self.assertEqual(response.status_code, 200)

    def test_admin_cant_reset_his_password(self):
        with self.client:
            response = self.admin_password_reset_identical_passwords()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'please provide a new password')

    def test_admin_cant_reset_his_passwords_with(self):
        with self.client:
            response = self.admin_password_reset_unmatching_passwords()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'],
                'new password doesnot match password_confirmation')

    def test_admin_cant_reset_his_password_with_an_invalid_new_password(self):
        with self.client:
            response = self.admin_password_reset_with_invalid_password()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'],
                'missing password/password should be atleast 4 characters')
