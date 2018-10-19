from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flasky.sale.model import Sale
from flasky.product.model import Product
from flasky.product.input_validation import is_sale_input_valid
from flasky.sale.manager import sale_manager
from flasky.response_helpers import sale_response, response
from flasky.response_helpers import convert_list_to_json, all_sales_response


sales_bp = Blueprint('sales', __name__, url_prefix='/api/v1')


class SaleRecordsView(MethodView):
    """
        A method view class to handle requests with the /sales endpoint
    """

    methods = ['POST', 'GET']

    def post(self):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response('request must be of type json', 'unsuccessful', 400)
        # extract request data
        request_data = request.get_json()
        attendant = request_data.get('attendant')
        # valid sale object input
        valid_input = is_sale_input_valid(attendant)
        if not isinstance(valid_input, bool):
            return response(valid_input, 'unsuccessful', 400)
        # create a new sale
        new_sale = Sale(attendant=attendant)
        # search and add products to a sale
        sale_manager.add_products(new_sale, 'macbook air')
        # save new sale object
        sale_manager.add_sale_record(new_sale)
        # return response with a new sale
        return sale_response(new_sale, 'successful', 201)


# Register a class as a view
sales = SaleRecordsView.as_view('sales')


# Add url_rules for the API endpoints
sales_bp.add_url_rule('/sales', view_func=sales)
