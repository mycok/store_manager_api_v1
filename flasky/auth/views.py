from flask import (Blueprint, request, abort)
from flask.views import MethodView

from flasky.auth.auth_helper_functions import (
    response_for_get_all_users, auth_success_response
    )
from flasky.response_helpers import (
    response
    )
from flasky.auth.user_model_controller import controller
from flasky.auth.user_model import User
from flasky.validator import Validation as v


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')


class SignUp(MethodView):
    """

    """
    methods = ['POST', 'GET']

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

        return response(
            new_user.username + ' has signed up', 'success', 201)


class Login(MethodView):
    """

    """
    @classmethod
    def post(cls):
        """[summary]
        """
        if not request.content_type == 'application/json':
            abort(400)

        sent_data = request.get_json()
        email = sent_data.get('email')
        password = sent_data.get('password')

        is_input_valid = v.validate_user_login(email=email, password=password)
        if not isinstance(is_input_valid, bool):
            return response(is_input_valid, 'unsuccessful', 400)

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


# Register a class as a view
signup = SignUp.as_view('register')
login = Login.as_view('login')


# Add url_rules for the API endpoints
auth_bp.add_url_rule('/auth/signup', view_func=signup)
auth_bp.add_url_rule('/auth/login', view_func=login)
