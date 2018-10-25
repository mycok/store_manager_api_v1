from flask import Blueprint, request
from flask.views import MethodView

from flasky.product.input_validation import is_valid_shopping_cart_product
from flasky.shopping_cart.shopping_cart_model import AddToCart as cart
from flasky.response_helpers import response


shopping_cart_bp = Blueprint('shopping_cart', __name__, url_prefix='/api/v1')


class ShoppingCartView(MethodView):
    """
    Method view class for posting products to add to the shopping cart
    """
    methods = ['POST']

    # post a product name to add to cart
    def post(self):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response('request must be of type json',
                            'unsuccessful', 400)
        # extract request data
        request_data = request.get_json()
        product_name = request_data.get('name')
        product_quantity = request_data.get('quantity')
        # validate product object input
        valid_input = is_valid_shopping_cart_product(
            product_name, product_quantity)
        if not isinstance(valid_input, bool):
            return response(valid_input, 'unsuccessful', 400)
        # fetch and add product to shopping cart
        inserted = cart.insert(product_name, product_quantity)
        if inserted is None:
            return response(
                'product ' + product_name + ' added to shopping cart',
                'successful', 201)
        return response(inserted, 'unsuccessful', 400)

# Register a class as a view
shopping_cart = ShoppingCartView.as_view('shopping_cart')

# Add url_rules for the API endpoints
shopping_cart_bp.add_url_rule('/shopping_cart', view_func=shopping_cart)
