from flask import (
    jsonify, make_response, request)
from functools import wraps

from flasky.auth.user_model import User
from flasky.auth.user_model_controller import UserController as controller
from flasky.auth.invalid_token_controller import TokenController
from flasky.response_helpers import response


# Auth decorator
def token_required(f):
    """Decorator function to restrict access
    to view functions to only authenticated users
    provided their auth tokens are valid.

    Arguments:
        fn {function} -- takes a function argument to decorate.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        message = None
        # if the request contains an authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            try:
                # try to extract the token
                token = auth_header.split(" ")[1]

            except IndexError:
                # if the token can't be extracted due to
                # an index out of range error
                return make_response(jsonify({
                    'status': 'unsuccessful',
                    'message': 'failed to extract a token. please provide a valid token'
                })), 403

        elif not token:
            # if there is no token in the request header
            return make_response(jsonify({
                'message': 'Missing a token'
            })), 401

        # call the token decode method of the user model
        # to get the initial user_id in order extract the
        # right user from the user table in the database
        blacklisted_token = TokenController.check_if_token_exists(
            token)
        if isinstance(blacklisted_token, dict):
            message = response(
                'token blacklisted, please login again', 'unsuccessful', 401)

        decoded_response = User.decode_auth_token(token)
        if 'token is invalid' in decoded_response:
            message = response(decoded_response, 'unsuccessful', 401)
        # extract the user from the
        # db and assign that user as an argument in the returned function
        current_user = controller.fetch_user_by_id(decoded_response)
        if current_user is None:
            message = response("user doesnot exist", 'unsuccessful', 401)
        if message is not None:
            return message

        return f(current_user, *args, **kwargs)

    return decorated_function


def is_admin_role(role):
    return role == 'Admin'


def is_attendant_role(role):
    return role == 'Attendant'
