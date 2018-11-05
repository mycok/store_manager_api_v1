from unittest import TestCase
import json

from flasky import create_app
from flasky.config import TestingConfig
from flasky.product.product_model import Product
from flasky.auth.user_model import User
from flasky.sale.sale_model import Sale
from flasky.auth.user_model_controller import UserController
from flasky.product.product_controller import Controller
from flasky.database.postgres import DataBase


class TestFixture(TestCase):
    """
    Test class template for test re-usable objects
    """

    def setUp(self):
        self.app = create_app(config_name=TestingConfig)
        self.db = DataBase()
        self.db.connect(dbname='postgres', user='postgres', password='1987')
        self.db.create_db_tables()
        self.client = self.app.test_client()
        self.product = Product('macbook', 'computers/laptops', 3, 1499.0)
        self.sale = Sale('prodigal')

    def tearDown(self):
        self.db.drop_tables()

    # auth helper methods
    def direct_register_admin(self):
        admin = User('kibuuka', 'Admin',
                     'me2@mail.com', 'dNa#$1236',)
        UserController.create_user(admin)

    def direct_register_attendant(self):
        attendant = User('michael', 'Attendant',
                         'aweso@try.net', '92&Va^rtyu4')
        UserController.create_user(attendant)

    def create_attendants(self, token):
        name = 'intent'
        role = 'Attendant'
        email = 'smth@try.com'
        password = 'tHis#1245f'
        return self.client.post(
            '/api/v2/auth/signup', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                (dict(username=name, role=role, email=email, password=password)))
        )

    def attendant_login(self):
        email = 'aweso@try.net'
        password = '92&Va^rtyu4'
        self.direct_register_attendant()
        return self.client.post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps((dict(email=email, password=password))))

    def create_attendants_with_invalid_input(self, token):
        name = 'intent'
        role = 'Attendant'
        email = 'smthtry.com'
        password = 'tHis#1245f'
        return self.client.post(
            '/api/v2/auth/signup', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                (dict(username=name, role=role, email=email, password=password)))
        )

    def cant_create_attendants_with_invalid_name(self, token):
        name = ' '
        role = 'Attendant'
        email = 'smth@try.com'
        password = 'tHis#1245f'
        return self.client.post(
            '/api/v2/auth/signup', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                (dict(username=name, role=role, email=email, password=password)))
        )

    def create_attendants_with_invalid_token(self):
        name = 'intent'
        role = 'Attendant'
        email = 'smthtry.com'
        password = 'tHis#1245f'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
        return self.client.post(
            '/api/v2/auth/signup', content_type='application/json',
            headers=dict(Authorization=token),
            data=json.dumps((dict(username=name, role=role, email=email, password=password))))

    def create_attendants_with_missing_token(self):
        name = 'intent'
        role = 'Attendant'
        email = 'smthtry.com'
        password = 'tHis#1245f'
        return self.client.post(
            '/api/v2/auth/signup', content_type='application/json',
            data=json.dumps((dict(username=name, role=role, email=email, password=password))))

    def user_login(self):
        email = 'me2@mail.com'
        password = 'dNa#$1236'
        self.direct_register_admin()
        return self.client.post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps((dict(email=email, password=password))))

    def invalid_user_login(self):
        email = 'me2@mail.com'
        password = 'dNa#$12'
        self.direct_register_admin()
        return self.client.post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps((dict(email=email, password=password))))

    def invalid_email_user_login_(self):
        email = 'me2mail.com'
        password = 'dNa#$1236'

        self.direct_register_admin()
        return self.client.post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps((dict(email=email, password=password))))

    def missing_password_user_login_(self):
        email = 'me2mail@mail.com'
        password = ''

        self.direct_register_admin()
        return self.client.post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps((dict(email=email, password=password))))

    def user_logout(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/auth/logout', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def invalid_logout(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        self.client.post(
            '/api/v2/auth/logout', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )
        return self.client.post(
            '/api/v2/auth/logout', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def logout_without_authourization_header(self):
        return self.client.post(
            '/api/v2/auth/logout', content_type='application/json')

    # Product Model helper methods
    def create_product(self):
        """
        send a POST request to create a product object
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/products', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='macbookair',
                                 category='computers',
                                 quantity=4, price=1499.0)))

    def cant_create_product_as_an_attendant(self):
        """
        send a POST request to create a product object
        """
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/products', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='macbookair',
                                 category='computers',
                                 quantity=4, price=1499.0)))

    def create_product_with_missing_attributes(self):
        """
        send a POST request to create a product object
        with missing required parameters.
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        return self.client.post(
            '/api/v2/products', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='Lenovo',
                                 category='computers/laptops',
                                 price=1499.0)))

    def create_product_with_wrong_content_type(self):
        """
        send a POST request to create a product object
        with invalid content type.
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/products', content_type='xml',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='Lenovo',
                                 category='computers/laptops',
                                 price=1499.0)))

    def create_product_with_an_empty_string(self):
        """
         Test unsuccessful POST request to
        create a product with an empty string
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/products',
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='  ',
                                 category='computers/laptops',
                                 quantity=4, price=1499.0)))

    def get_all_products(self):
        """
        send a GET request to fetch all products
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.get(
            '/api/v2/products', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

    def invalid_fetch_product(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        _ = self.create_product()

        # get that product by id
        return self.client.get(
            '/api/v2/products/3',
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def fetch_product(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        product_response = self.create_product()
        data = json.loads(product_response.data.decode())
        product_id = data['product_id']

        # get that product by id
        return self.client.get(
            '/api/v2/products/{}'.format(product_id),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def update_product(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        product_response = self.create_product()
        data = json.loads(product_response.data.decode())
        product_id = data['product_id']

        # get that product by id
        return self.client.put(
            '/api/v2/products/{}'.format(product_id),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='macbookair',
                                 category='computers',
                                 quantity=70, price=1499.0)))

    def cant_update_product_as_an_attendant(self):
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        product_response = self.create_product()
        data = json.loads(product_response.data.decode())
        product_id = data['product_id']

        # get that product by id
        return self.client.put(
            '/api/v2/products/{}'.format(product_id),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='macbookair',
                                 category='computers',
                                 quantity=70, price=1499.0)))

    def cant_update_product_with_invalid_content_type(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        product_response = self.create_product()
        data = json.loads(product_response.data.decode())
        product_id = data['product_id']

        # get that product by id
        return self.client.put(
            '/api/v2/products/{}'.format(product_id),
            content_type='xml',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(name='macbookair',
                                 category='computers',
                                 quantity=70, price=1499.0)))

    def delete_product(self):
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']
        # post a product
        product_response = self.create_product()
        data = json.loads(product_response.data.decode())
        product_id = data['product_id']

        # get that product by id
        return self.client.delete(
            '/api/v2/products/{}'.format(product_id),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

# sale helper methods
    def create_sale(self):
        """
        send a POST request to create a sale object
        """
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                dict(attendant='michael')))

    def create_sale_as_admin(self):
        """
        send a POST request to create a sale object as an admin
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                dict(attendant='michael')))

    def create_sale_with_invalid_previllages(self):
        """
        send a POST request to create a sale object
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(
                dict(attendant='michael')))

    def create_sale_without_the_attendant_attribute(self):
        """
        send a POST request to create a sale object
        with  a missing required parameter.
        """
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps(dict(attendant='  ')))

    def create_sale_with_wrong_content_type(self):
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.post(
                '/api/v2/sales',
                content_type="xml",
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(attendant='ivan')))

    def get_all_sales(self):
        """
        send a GET request to fetch all sales
        """
        response = self.user_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.get(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

    def get_all_sales_without_a_token(self):
        """
        send a GET request to fetch all sales
        """
        return self.client.get(
            '/api/v2/sales', content_type='application/json')

    def get_all_sales_as_an_attendant(self):
        """
        send a GET request to fetch all sales
        """
        response = self.attendant_login()
        data = json.loads(response.data.decode())
        token = data['token']

        return self.client.get(
            '/api/v2/sales', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

# shopping cart helper methods
    def add_product_to_cart(self):
        """
        send a POST request to add a product to cart
        """
        response = self.create_product()
        data = json.loads(response.data.decode())
        prod_id = data['product_id']
        return self.client.post(
            '/api/v2/cart', content_type='application/json',
            data=json.dumps(dict(product_id=prod_id, quantity=4))
        )
