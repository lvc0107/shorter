from functools import wraps
from werkzeug.exceptions import Unauthorized
from flask import current_app, request


def get_user_information_from_id_provider(token):
    # call ID provider, sending a decoded JWT
    # Mocked response
    response_json = {}
    if token == "admin_token":
        response_json["username"] = "admin_user"
        response_json["email"] = "admin@shorter_app.com"
        response_json["type"] = "admin"
    elif token == "consumer_token":
        response_json["username"] = "consumer_user"
        response_json["email"] = "consumer@shorter_app.com"
        response_json["type"] = "consumer"
    else:
        response_json["username"] = None
        response_json["email"] = None
        response_json["type"] = "invalid_user"

    return response_json


class AuthenticatedUser:
    def __init__(self, token):
        response_json = get_user_information_from_id_provider(token)
        self.username = response_json["username"]
        self.email = response_json["email"]
        self.type = response_json["type"]
        self.is_admin = self.type == "admin"
        self.is_consumer = self.type == "consumer"


def get_bearer_token():
    auth_header = request.headers.get("authorization")
    return (
        auth_header[7:] if auth_header and auth_header.startswith("Bearer ") else None
    )


def init_user():
    current_app.user = None
    token = get_bearer_token()
    if token:
        current_app.user = AuthenticatedUser(token)


def get_user():
    return current_app.user


def authorized_user(admin=False, consumer=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_user()
            if user and admin and user.is_admin:
                return func(*args, **kwargs)
            if user and consumer and user.is_consumer:
                return func(*args, **kwargs)
            raise Unauthorized

        return wrapper

    return decorator
