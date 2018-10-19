from flask import Flask
from flasky.config import DevelopmentConfig
from flasky.product.views import products_bp


def create_app(config_name=None):

    app = Flask(__name__)
    if config_name is not None:
        app.config.from_object(config_name)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(products_bp)
    return app
