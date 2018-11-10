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
from flasky.auth.auth_decorator import (
    token_required, is_admin_role
)


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v2')


class SignUp(MethodView):

    methods = ['POST', 'PUT']

    decorators = [token_required]

    @classmethod
    def post(cls, current_user):
        # check request content type
        if not request.content_type == 'application/json':
            abort(400, 'request must be of type json')
        # check user role
        if not is_admin_role(current_user.role):
            return response('Admin previllages required', 'unsuccessful', 401)
        # extract request data
        sent_data = request.get_json()
        username = sent_data.get('username')
        role = sent_data.get('role')
        email = sent_data.get('email')
        password = sent_data.get('password')
        # validate input
        is_input_valid = v.validate_user(username, email, password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 400)
        # Create a new user from the provided input
        new_user = User(username=username,
                        role=role, email=email, password=password)
        # Check the new_user already exists
        existing_user = controller.check_if_user_exists(email)
        if existing_user is not None:
            return response(
                'user with email {} already exists'.format(existing_user['email']),
                'unsuccessful', 400)
        # save new user to the database
        controller.create_user(new_user)
        # return a success response
        return create_user_response(
            new_user, url_for('auth.signup', name=new_user.username))

    @classmethod
    def put(cls, current_user):
        # check request content type
        if not request.content_type == 'application/json':
            abort(400, 'request must be of type json')
        # check user role
        if not is_admin_role(current_user.role):
            return response('Admin previllages required', 'unsuccessful', 401)
        # extract request data
        sent_data = request.get_json()
        username = sent_data.get('username')
        role = sent_data.get('role')
        email = sent_data.get('email')
        password = sent_data.get('password')
        # validate input
        is_input_valid = v.validate_user(username, email, password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 400)
        # Check the new_user already exists
        existing_user = controller.check_if_user_exists(email)
        if existing_user is not None:
            updated = controller.update_user_role(role, email)
            if isinstance(updated, dict):
                return response(updated, 'successful', 200)
            return response(updated, 'unsuccessful', 400)
        return response(
            'user with email ' + email + ' doesnot exist',
            'unsuccessful', 400)


class Login(MethodView):

    methods = ['POST']

    @classmethod
    def post(cls):
        # check request content type
        if not request.content_type == 'application/json':
            abort(400)
        # extract request data
        sent_data = request.get_json()
        email = sent_data.get('email')
        password = sent_data.get('password')
        # validate input
        is_input_valid = v.validate_user_login(email=email, password=password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 401)
        # Check the user already exists
        existing_user = controller.check_if_user_exists(email)
        if existing_user is None:
            return response(
                'user with email ' + email + ' doesnot exist',
                'unsuccessful', 401)
        # verify password
        if not User.check_password(existing_user['password'], password):
            return response(
                'provided password is incorrect', 'unsuccessful', 401)
        # generate jwt token
        token = User.generate_auth_token(existing_user['user_id'])
        if not isinstance(token, bytes):
            return response(str(token), 'unsuccessful', 401)
        # return a success response
        return auth_success_response(
           existing_user['username'] + ' is now logged in', token)


class Logout(MethodView):

    methods = ['POST']

    @classmethod
    def post(cls):
        # check for token in request header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response(
                'Provide an authorization header', 'unsuccessful', 403)
        try:
            # extract token from request header
            auth_token = auth_header.split(" ")[1]

        except IndexError:
            return response('unable to extract token', 'unsuccessful', 403)

        # check if the token is already blacklisted
        is_token_invalid = TokenController.check_if_token_exists(
            auth_token)

        if isinstance(is_token_invalid, dict):
            return response(
                'token already invalidated', 'unsuccessful', 400)
        # blacklist/invalidate token
        token = InvalidToken(auth_token)
        # save blacklisted token to a databse
        TokenController.save_invalid_token(token)
        return response('successfully logged out', 'success', 200)


# Register a class as a view
signup = SignUp.as_view('signup')
login = Login.as_view('login')
logout = Logout.as_view('logout')


# Add url_rules for the API endpoints
auth_bp.add_url_rule('/auth/signup', view_func=signup)
auth_bp.add_url_rule('/auth/login', view_func=login)
auth_bp.add_url_rule('/auth/logout', view_func=logout)
