from flask import (
    Blueprint, request, url_for)
from flask.views import MethodView

from flasky.product.product_model import Product
from flasky.validator import Validation as v
from flasky.product.product_controller import Controller
from flasky.response_helpers import (
    create_resource_response, response,
    single_product_response, fetch_all_response,
    convert_list_to_json
)
from flasky.auth.auth_decorator import (
    token_required, is_admin_role, is_attendant_role
)


products_bp = Blueprint('products', __name__, url_prefix='/api/v2')


class ProductListView(MethodView):
    """
    A method view class to handle requests with the /products endpoint
    """

    methods = ['POST', 'GET']

    # decorators = [token_required]

    # create a product
    @classmethod
    def post(cls):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response('request must be of type json',
                            'unsuccessful', 400)
        # if not is_admin_role(current_user.role):
        #     return response('Admin previllages required', 'unsuccessful', 401)

        # extract request data
        request_data = request.get_json()
        name = request_data.get('name')
        category = request_data.get('category')
        quantity = request_data.get('quantity')
        price = request_data.get('price')
        # validate product object input
        valid_input = v.validate_product(name=name, category=category, quantity=quantity, price=price)
        if not isinstance(valid_input, bool):
            return response(valid_input, 'unsuccessful', 400)
        # create a new product
        new_product = Product(name=name, category=category,
                              quantity=quantity, price=price)
        # check if a product with the same name already exists
        existing_product = Controller.add_product(new_product)
        if existing_product is not None:
            return response(existing_product, 'unsuccessful', 400)
        # return response with a new product
        return create_resource_response(
            new_product,
            url_for('products.product', product_id=new_product.product_id))

    # fetch all products
    @classmethod
    def get(cls):

        products = Controller.fetch_all_products()
        if isinstance(products, str):
            return response(products, 'unsuccessful', 200)
        return fetch_all_response(products, 'products')


class ProductView(MethodView):
    """
    A method view class to handle requests with
    /products/<int:product_id> endpoint
    """

    methods = ['GET', 'PUT', 'DELETE']

    # decorators = [token_required]

    @classmethod
    def get(cls, product_id):
        # GET request to fetch a product by id
        product = Controller.fetch_product_by_id(product_id)
        if not isinstance(product, dict):
            return response(product, 'unsuccessful', 400)
        return response(product, 'successful', 200)

    # PUT
    @classmethod
    def put(cls, product_id):
        """
        PUT request to update contents
        of a product by id

        Arguments:
            PRODUCT_id --int-- A unique integer id assigned to a single product
        """
        if not request.content_type == 'application/json':
            return response('request must be of type json', 'failed', 400)
        # if not is_admin_role(current_user.role):
        #     return response('Admin previllages required', 'unsuccessful', 401)

        sent_data = request.get_json()
        name = sent_data.get('name')
        category = sent_data.get('category')
        quantity = sent_data.get('quantity')
        price = sent_data.get('price')

        # query the database through a manager object
        updated = Controller.update_product(
            name, category, quantity, price, product_id)
        if updated is None:
            return response(updated, 'unsuccessful', 400)
        return response(str(updated) + ' row successfully updated', 'success', 200)

    # DELETE
    @classmethod
    def delete(cls, product_id):
        """
        DELETE request to delete a product by id

        Arguments:
            product_id --int-- A unique integer id assigned to a single product
        """
        if not request.content_type == 'application/json':
            return response('request must be of type json', 'failed', 400)
        # if not is_admin_role(current_user.role):
        #     return response('Admin previllages required', 'unsuccessful', 401)

        # delete the product
        deleted = Controller.delete_product_by_id(product_id)
        if deleted is not None:
            return response(
                'product with ID {0} has been deleted'.format(product_id),
                'successful', 200)
        # otherwise return a string response
        return response("product doesnot exist", "unsuccessful", 400)


# Register a class as a view
products = ProductListView.as_view('products')
product = ProductView.as_view('product')


# Add url_rules for the API endpoints
products_bp.add_url_rule('/products', view_func=products)
products_bp.add_url_rule('/products/<int:product_id>', view_func=product)
