from flask import make_response, jsonify


# Response helpers
def auth_success_response(message, token):
    return make_response(jsonify({
        'message': message,
        'status': 'success',
        'token': token.decode('utf-8')
    })), 200


def create_user_response(user, resource_url):
    return make_response(jsonify({
        'message': '{} has signed up'.format(user.username),
        'status': 'successful',
        'resource_link': resource_url
    })), 201
