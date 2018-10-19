from flask import Flask
from flasky.config import DevelopmentConfig


def create_app(config_name=None):

    app = Flask(__name__)
    if config_name is not None:
        app.config.from_object(config_name)
    app.config.from_object(DevelopmentConfig)
    return app
