from flask import Blueprint, request
from flask.views import MethodView

from flasky.sale.sale_model import Sale
from flasky.validator import Validation as v
from flasky.sale.sale_controller import controller
from flasky.shopping_cart.shopping_cart_model import AddToCart as cart
from flasky.response_helpers import single_sale_response, response
from flasky.response_helpers import convert_list_to_json, all_sales_response


sales_bp = Blueprint('sales', __name__, url_prefix='/api/v1')


class SaleRecordsView(MethodView):

    # A method view class to handle requests with the /sales endpoint

    methods = ['POST', 'GET']

    # create a sale
    @classmethod
    def post(cls):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response(
                'request must be of type json', 'unsuccessful', 400)
        # extract request data
        request_data = request.get_json()
        attendant = request_data.get('attendant')
        # validate sale object input
        valid_sale_input = v.validate_sale(attendant)
        if not isinstance(valid_sale_input, bool):
            return response(valid_sale_input, 'unsuccessful', 400)
        # create a new sale
        new_sale = Sale(attendant=attendant)
        # update the new_sale's products list with new products
        products = cart.load_shopping_cart()
        new_sale.products += products
        # update product attributes
        cart.update_sale_attributes(new_sale)
        # save new sale object
        controller.add_sale_record(new_sale)
        # return response with a new sale
        return single_sale_response(new_sale, 'successful', 201)

    # fetch all sales
    @classmethod
    def get(cls):
        sales = controller.fetch_all_sale_records()
        if not isinstance(sales, list):
            return response(sales, 'unsuccessful', 400)
        return all_sales_response(
            convert_list_to_json(sales), 'successful', 200)


class SaleView(MethodView):

    methods = ['GET']

    @classmethod
    def get(cls, sale_id):
        # GET request to fetch a sale by id
        sale = controller.fetch_sale_record(sale_id)
        if not isinstance(sale, Sale):
            return response(sale, 'unsuccessful', 400)
        return single_sale_response(sale, 'successful', 200)


# Register a class as a view
sales = SaleRecordsView.as_view('sales')
sale = SaleView.as_view('sale')


# Add url_rules for the API endpoints
sales_bp.add_url_rule('/sales', view_func=sales)
sales_bp.add_url_rule('/sales/<int:sale_id>', view_func=sale)
