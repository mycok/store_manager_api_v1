from flask import make_response, jsonify, request


# Response helpers
def auth_success_response(message, token):
    return make_response(jsonify({
        'message': message,
        'status': 'success',
        'token': token.decode('utf-8')
    })), 200


def response_for_get_all_users(users, status_code):
    return make_response(jsonify({
        'status': 'success',
        'users': users
    })), status_code


def convert_user_tuple_to_list(tup):
    """
    converts a list to json
    Arguments:
        lst -- list of objects
    """

    lst = list(tup)
    # lst.pop(0)
    return lst
