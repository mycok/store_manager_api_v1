from flask import Flask

from flasky.config import DevelopmentConfig
from flasky.product.product_view import products_bp
from flasky.sale.sale_view import sales_bp
from flasky.shopping_cart.shopping_cart_view import shopping_cart_bp


def create_app(config_name=None):

    app = Flask(__name__)
    if config_name is not None:
        app.config.from_object(config_name)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(products_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(shopping_cart_bp)
    return app
