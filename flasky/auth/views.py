from flask import (Blueprint, request, abort, url_for)
from flask.views import MethodView

from flasky.auth.auth_helper_functions import (
    auth_success_response, create_user_response
    )
from flasky.response_helpers import response
from flasky.auth.user_model_controller import UserController as controller
from flasky.auth.invalid_token_controller import TokenController

from flasky.auth.user_model import User
from flasky.auth.invalid_token_model import InvalidToken
from flasky.validator import Validation as v


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')


class SignUp(MethodView):

    methods = ['POST']

    @classmethod
    def post(cls):
        if not request.content_type == 'application/json':
            abort(400)

        sent_data = request.get_json()
        username = sent_data.get('username')
        role = sent_data.get('role')
        email = sent_data.get('email')
        password = sent_data.get('password')

        is_input_valid = v.validate_user(username, email, password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 400)
        # Create a new user
        new_user = User(username=username,
                        role=role, email=email, password=password)
        # Check the new_user already exists
        existing_user = controller.check_if_user_exists(email)
        if existing_user is not None:
            return response('user with email ' + existing_user['email'] + ' already exists', 'unsuccessful', 400)

        controller.create_user(new_user)

        return create_user_response(
            new_user, url_for('auth.register', email=new_user.email))


class Login(MethodView):

    methods = ['POST']

    @classmethod
    def post(cls):

        if not request.content_type == 'application/json':
            abort(400)

        sent_data = request.get_json()
        email = sent_data.get('email')
        password = sent_data.get('password')

        is_input_valid = v.validate_user_login(email=email, password=password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 401)

        existing_user = controller.check_if_user_exists(email)
        if existing_user is None:
            return response(
                'user with email ' + email + ' doesnot exist',
                'unsuccessful', 401)

        if not User.check_password(existing_user['password'], password):
            return response(
                'provided password is incorrect', 'unsuccessful', 401)

        token = User.generate_auth_token(existing_user['user_id'])
        if not isinstance(token, bytes):
            return response(str(token), 'unsuccessful', 401)
        return auth_success_response(
           existing_user['username'] + ' is now logged in', token)


class Logout(MethodView):

    methods = ['POST']

    @classmethod
    def post(cls):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response(
                'Provide an authorization header', 'unsuccessful', 403)
        try:
            auth_token = auth_header.split(" ")[1]

        except IndexError:
            return response('unable to extract token', 'unsuccessful', 403)
        else:
            decoded_token_response = User.decode_auth_token(auth_token)

            if not isinstance(decoded_token_response, int):
                return response(decoded_token_response, 'unsuccessful', 401)
            is_token_invalid = TokenController.check_if_token_exists(
                auth_token)

            if isinstance(is_token_invalid, list):
                return response(
                    'token already invalidated', 'unsuccessful', 400)
            token = InvalidToken(auth_token)

            TokenController.save_invalid_token(token)
            return response('successfully logged out', 'success', 200)


# Register a class as a view
signup = SignUp.as_view('register')
login = Login.as_view('login')
logout = Logout.as_view('logout')


# Add url_rules for the API endpoints
auth_bp.add_url_rule('/auth/signup', view_func=signup)
auth_bp.add_url_rule('/auth/login', view_func=login)
auth_bp.add_url_rule('/auth/logout', view_func=logout)
