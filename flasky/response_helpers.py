from flask import make_response, jsonify


# general custom response
def response(message, status, status_code):
    return make_response(jsonify({
        "message": message,
        "status": status
    })), status_code


# product custom responses
def single_product_response(product):
    return make_response(jsonify({
        'product_id': product.product_id,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'in_stock': product.quantity,
        'sales': product.sales,
        'status': 'success'
    })), 200


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


def all_products_response(products, status, status_code):
    return make_response(jsonify({
        'products': products,
        'status': status
    })), status_code


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


# converters
def convert_list_to_json(list_object):

    """
    converts the provided list into a list of dictionaries by
    alterating through the provided list object
    and calling the to_json model method to create
    a dictionary representation of the model object then
    append the list to dict_list.

    Arguments:
        lst -- list of objects
    """
    dict_list = []
    for lst in list_object:
        dict_list.append(lst.to_json())
    return dict_list
