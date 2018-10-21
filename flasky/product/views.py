from flask import Blueprint, request
from flask.views import MethodView
from flasky.product.model import Product
from flasky.product.input_validation import is_product_input_valid
from flasky.product.manager import product_manager
from flasky.response_helpers import product_response, response
from flasky.response_helpers import convert_list_to_json, all_list_response


products_bp = Blueprint('products', __name__, url_prefix='/api/v1')


class ProductListView(MethodView):
    """
        A method view class to handle requests with the /products endpoint
    """

    methods = ['POST', 'GET']

    # create a product
    def post(self):
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
        # valid product object input
        valid_input = is_product_input_valid(name, category, quantity, price)
        if not isinstance(valid_input, bool):
            return response(valid_input, 'unsuccessful', 400)
        # create a new product
        new_product = Product(name=name, category=category, quantity=quantity, price=price)
        # check if a product with the same name already exists
        is_existing_product = product_manager.add_product(new_product)
        if not isinstance(is_existing_product, bool):
            return response(is_existing_product, 'unsuccessful', 400)
        # return response with a new product
        return product_response(new_product, 201)

    # fetch all products
    def get(self):

        products = product_manager.fetch_all_products()
        if isinstance(products, str):
            return response(products, 'unsuccessful', 400)
        return all_list_response(convert_list_to_json(products), 'successful', 200)


class ProductView(MethodView):
    """
        A method view class to handle requests with /products/<int:id endpoint
    """

    methods = ['GET']

    def get(self, p_id):
        # GET request to fetch a product by id
        product = product_manager.fetch_product(p_id)
        if not isinstance(product, Product):
            return response(product, 'unsuccessful', 400)
        return product_response(product, 200)


# Register a class as a view
products = ProductListView.as_view('products')
product = ProductView.as_view('product')


# Add url_rules for the API endpoints
products_bp.add_url_rule('/products', view_func=products)
products_bp.add_url_rule('/products/<int:p_id>', view_func=product)
