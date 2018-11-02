from flask import Blueprint, request
from flask.views import MethodView

from flasky.validator import Validation as v
from flasky.cart.cart_controller import AddToCart
from flasky.response_helpers import response


cart_bp = Blueprint('shopping_cart', __name__, url_prefix='/api/v2')


class CartView(MethodView):
    """
    Method view class for posting products to add to the cart
    """
    methods = ['POST']

    # post a product name to add to cart
    @classmethod
    def post(cls):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response('request must be of type json',
                            'unsuccessful', 400)
        # extract request data
        request_data = request.get_json()
        product_id = request_data.get('product_id')
        product_quantity = request_data.get('quantity')

        # fetch and add product to shopping cart
        inserted = AddToCart.insert(product_id, product_quantity)
        if not isinstance(inserted, str):
            return response(
                'product ' + str(product_id) + ' added to shopping cart',
                'successful', 201)
        return response(inserted, 'unsuccessful', 400)

# Register a class as a view
cart = CartView.as_view('cart')

# Add url_rules for the API endpoints
cart_bp.add_url_rule('/cart', view_func=cart)
