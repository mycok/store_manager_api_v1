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
                    'status': 'Failed to extract token',
                    'message': 'Please provide a valid token'
                })), 403

        if not token:
            # if there is no token in the request header
            return make_response(jsonify({
                'message': 'Missing a token'
            })), 401

        try:
            # call the token decode method of the user model
            # to get the initial user_id in order extract the
            # right user from the user table in the database
            blacklisted_token = TokenController.check_if_token_exists(token)
            if isinstance(blacklisted_token, list):
                return response(
                    'token blacklisted, please login again', 'unsuccessful',
                    401)
            decoded_response = User.decode_auth_token(token)
            user = controller.fetch_user_by_id(decoded_response)
            current_user = User(
                username=user['username'], role=user['role'],
                email=user['email'], password=user['password_hash']
                )
        except:
            # if the token has been already used to logout which
            # makes it invalid, the function will raise an error
            message = 'Invalid token'
            if isinstance(decoded_response, str):
                message = decoded_response
            return make_response(jsonify({
                'status': 'Failed to extract user_id',
                'message': message
            })), 401
        # extract the user from the
        # db and assign that user as an argument in the returned function
        return f(current_user, *args, **kwargs)

    return decorated_function
