from flask import make_response, jsonify, url_for


def response(message, status, status_code):
    return make_response(jsonify({
        "message": message,
        "status": status
    })), status_code

# product custom responses
def product_response(product, status_code):
    return make_response(jsonify({
        'p_id': product.p_id,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'quantity': product.quantity,
        'sales': product.sales
    })), status_code


def all_list_response(products, status, status_code):
    return make_response(jsonify({
        'products': products,
        'status': status
    })), status_code


# sale custom responses
def sale_response(sale, status, status_code):
    return make_response(jsonify({
        'sale_id': sale.sale_id,
        'attendant': sale.attendant,
        'products': sale.products,
        'status': status
    })), status_code


def all_sales_response(sales, status, status_code):
    return make_response(jsonify({
        'sales': sales,
        'status': status
    })), status_code


# converters
def convert_list_to_json(lsty):

        """
    converts a list to json
    Arguments:
        lst -- list of objects
    """
        lst = []
        for l in lsty:
            lst.append(l.to_json())
        return lst
