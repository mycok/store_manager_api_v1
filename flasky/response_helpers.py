from flask import make_response, jsonify


# general custom response
def response(message, status, status_code):
    return make_response(jsonify({
        "message": message,
        "status": status
    })), status_code


# product custom responses
def create_resource_response(resource, resource_url):
    return make_response(jsonify({
        'message': '{} has been added'.format(resource.name),
        'status': 'successful',
        'product_id': resource.product_id,
        'resource_link': resource_url
    })), 201


def fetch_all_response(resource, resource_name):
    return make_response(jsonify({
        '{}'.format(resource_name): resource,
        'status': 'successful'
    })), 200


# sale custom responses
def single_sale_response(sale, status_code):
    return make_response(jsonify({
        'sale_id': sale.sale_id,
        'attendant': sale.attendant,
        'products': sale.products,
        'total_products': sale.total_products,
        'total_amount': sale.total_amount,
        'status': 'success'
    })), status_code


def all_sales_response(sales, status, status_code):
    return make_response(jsonify({
        'sales': sales,
        'status': status
    })), status_code
