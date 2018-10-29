from flask import Blueprint, request
from flask.views import MethodView

from flasky.product.product_model import Product
from flasky.validator import Validation as v
from flasky.product.product_controller import controller
from flasky.response_helpers import single_product_response, response
from flasky.response_helpers import convert_list_to_json, all_products_response


products_bp = Blueprint('products', __name__, url_prefix='/api/v1')


class ProductListView(MethodView):

    # class to handle requests to /products endpoint

    methods = ['POST', 'GET']

    # create a product
    @classmethod
    def post(cls):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response('request must be of type json',
                            'unsuccessful', 400)
        # extract request data
        request_data = request.get_json()
        name = request_data.get('name')
        category = request_data.get('category')
        quantity = request_data.get('quantity')
        price = request_data.get('price')
        # validate product object input
        valid_input = v.validate_product(name, category, quantity, price)
        if not isinstance(valid_input, bool):
            return response(valid_input, 'unsuccessful', 400)
        # create a new product
        new_product = Product(name=name, category=category,
                              quantity=quantity, price=price)
        # check if a product with the same name already exists
        is_existing_product = controller.add_product(new_product)
        if not isinstance(is_existing_product, bool):
            return response(is_existing_product, 'unsuccessful', 400)
        # return response with a new product
        return single_product_response(new_product, 'successful', 201)

    # fetch all products
    @classmethod
    def get(cls):

        products = controller.fetch_all_products()
        if isinstance(products, str):
            return response(products, 'unsuccessful', 200)
        return all_products_response(
            convert_list_to_json(products), 'successful', 200)


class ProductView(MethodView):

    # class to handle requests to /products/<int:product_id>


    methods = ['GET']

    @classmethod
    def get(cls, product_id):
        # GET request to fetch a product by id
        product = controller.fetch_product_by_id(product_id)
        if not isinstance(product, Product):
            return response(product, 'unsuccessful', 400)
        return single_product_response(product, 'successful', 200)


# Register a class as a view
products = ProductListView.as_view('products')
product = ProductView.as_view('product')


# Add url_rules for the API endpoints
products_bp.add_url_rule('/products', view_func=products)
products_bp.add_url_rule('/products/<int:product_id>', view_func=product)
