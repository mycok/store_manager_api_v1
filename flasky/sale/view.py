from flask import Blueprint, request
from flask.views import MethodView
from flasky.sale.model import Sale
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

    # create a sale
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

    # fetch all sales
    def get(self):
        sales = sale_manager.fetch_all_sale_records()
        if not isinstance(sales, list):
            return response(sales, 'unsuccessful', 400)
        return all_sales_response(convert_list_to_json(sales), 'successful', 200)


class SaleView(MethodView):
    """
        A method view class to handle requests with /sales/<int:id>
        endpoint
    """

    methods = ['GET']

    def get(self, sale_id):
        # GET request to fetch a product by id
        sale = sale_manager.fetch_sale_record(sale_id)
        if not isinstance(sale, Sale):
            return response(sale, 'unsuccessful', 400)
        return sale_response(sale, 'successful', 200)


# Register a class as a view
sales = SaleRecordsView.as_view('sales')
sale = SaleView.as_view('sale')


# Add url_rules for the API endpoints
sales_bp.add_url_rule('/sales', view_func=sales)
sales_bp.add_url_rule('/sales/<int:sale_id>', view_func=sale)