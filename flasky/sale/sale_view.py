from flask import (Blueprint, request, jsonify)
from flask.views import MethodView
import json

from flasky.sale.sale_model import Sale
from flasky.validator import Validation as v
from flasky.cart.cart_controller import AddToCart
from flasky.sale.sale_controller import Controller
from flasky.response_helpers import (single_sale_response,
                                     response,
                                     all_sales_response,
                                     fetch_all_response)

from flasky.auth.auth_decorator import (
    token_required, is_admin_role, is_attendant_role
)


sales_bp = Blueprint('sales', __name__, url_prefix='/api/v2')


class SaleRecordsView(MethodView):

    # A method view class to handle requests with the /sales endpoint
    methods = ['POST', 'GET']

    decorators = [token_required]

    # create a sale
    @classmethod
    def post(cls, current_user):
        # check for a valid content type
        if not request.content_type == 'application/json':
            return response(
                'request must be of type json', 'unsuccessful', 400)

        if not is_attendant_role(current_user['role']):
            return response('Attendant previllages required',
                            'unsuccessful', 401)
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
        products = AddToCart.load_cart()
        if not isinstance(products, list) or len(products) == 0:
            return response('please add products to cart', 'unsuccessful', 400)

        new_sale.products += products
        # update product attributes
        AddToCart.update_sale_attributes(new_sale, products)
        # save new sale object
        Controller.add_sale_record(new_sale)
        new_sale.products = [json.loads(product)
                             for product in new_sale.products]
        # return response with a new sale
        return single_sale_response(new_sale, 201)

    # fetch all sales
    @classmethod
    def get(cls, current_user):
        if not is_admin_role(current_user['role']):
            return response('Admin previllages required', 'unsuccessful', 401)

        sales = Controller.fetch_all_sale_records()
        if not isinstance(sales, list):
            return response(sales, 'unsuccessful', 400)

        for index, sale in enumerate(sales):
            sales[index]['products'] = [json.loads(product) for product in sale['products']]

        return all_sales_response(sales, 'successful', 200)


class SaleView(MethodView):

    methods = ['GET']

    decorators = [token_required]

    @classmethod
    def get(cls, current_user, sale_id):
        # GET request to fetch a sale by id
        if not is_admin_role(current_user['role']):
            return response('Admin previllages required', 'unsuccessful', 401)

        sale = Controller.fetch_sale_record(sale_id)
        if not isinstance(sale, dict):
            return response(sale, 'unsuccessful', 400)
        print(sale)

        sale['products'] = [json.loads(product)
                            for product in sale['products']]

        return jsonify(sale, 'success'), 200


class SaleAttendant(MethodView):

    methods = ['GET']

    decorators = [token_required]

    @classmethod
    def get(cls, current_user, attendant):
        # GET request to fetch a sale by attendant
        sales = Controller.fetch_sale_record_by_attendant(attendant)
        if isinstance(sales, str):
            return response(sales, 'unsuccessful', 400)

        for index, sale in enumerate(sales):
            sales[index] = [json.loads(product)
                            for product in sale['products']]

        return all_sales_response((sales), 'successful', 200)


# Register a class as a view
sales = SaleRecordsView.as_view('sales')
sale = SaleView.as_view('sale')
sale_attendant = SaleAttendant.as_view('sale_attendant')


# Add url_rules for the API endpoints
sales_bp.add_url_rule('/sales', view_func=sales)
sales_bp.add_url_rule('/sales/<int:sale_id>', view_func=sale)
sales_bp.add_url_rule('/sales/<string:attendant>', view_func=sale_attendant)
