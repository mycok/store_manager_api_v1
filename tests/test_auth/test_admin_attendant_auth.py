from tests.fixture import TestFixture
import json


class TestAdminSignUp(TestFixture):
    def test_admin_can_successfully_create_an_attendant(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            response = self.create_attendants(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_admin_cant_create_already_existing_attendant(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            _ = self.create_attendants(token)
            response = self.create_attendants(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'user with email smth@try.com already exists')

    def test_admin_cant_create_attendant_with_invalid_email(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            response = self.create_attendants_with_invalid_input(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'invalid email or missing email address')

    def test_admin_cant_create_attendant_with_invalid_name(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            response = self.cant_create_attendants_with_invalid_name(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'], 'Please provide the correct name and/or username')

    def test_admin_can_successfully_assign_admin_role_an_attendant(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            response = self.create_attendants(token)
            self.assertEqual(response.status_code, 201)

            update_response = self.edit_attendants(token)
            self.assertEqual(update_response.status_code, 200)

    def test_admin_cant_assign_admin_role_an_attendant(self):
        with self.client:
            resp = self.user_login()
            data = json.loads(resp.data.decode())
            token = data['token']

            response = self.create_attendants(token)
            self.assertEqual(response.status_code, 201)

            update_response = self.cant_edit_attendants(token)
            data = json.loads(update_response.data.decode())
            self.assertEqual(update_response.status_code, 400)
            self.assertEqual(
                data['message'], 'user with email smth@tryy.com doesnot exist')


class TestAdmin_Attendant_Login(TestFixture):
    def test_admin_attendant_login(self):
        with self.client:
            response = self.user_login()
            self.assertEqual(response.status_code, 200)

    def test_admin_attendant_cant_login_with_unmatching_passwords(self):
        with self.client:
            response = self.invalid_user_login()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                data['message'], 'provided password is incorrect')

    def test_admin_attendant_cant_login_with_invalid_password(self):
        with self.client:
            response = self.invalid_user_login()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                data['message'], 'provided password is incorrect')

    def test_admin_attendant_cant_login_without_a_password(self):
        with self.client:
            response = self.missing_password_user_login_()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                data['message'], 'missing password/password should be atleast 4 characters')

    def test_admin_attendant_cant_login_with_invalid_email(self):
        with self.client:
            response = self.invalid_email_user_login_()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                data['message'], 'invalid email or missing email address')

    def test_admin_cant_signup_or_loginwith_an_invalid_token(self):
        with self.client:
            response = self.create_attendants_with_invalid_token()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertEqual(data['message'], 'failed to extract a token. please provide a valid token')

    def test_admin_cant_signup_or_login_without_a_token(self):
        with self.client:
            response = self.create_attendants_with_missing_token()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'], 'Missing a token')


class TestAdmin_Attendant_Logout(TestFixture):
    def test_successful_logout(self):
        with self.client:
            response = self.user_logout()
            self.assertEqual(response.status_code, 200)

    def test_cant_logout_with_a_blacklisted_token(self):
        with self.client:
            response = self.invalid_logout()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'token already invalidated')

    def test_cant_logout_without_a_token(self):
        with self.client:
            response = self.logout_without_authourization_header()
            self.assertEqual(response.status_code, 403)
