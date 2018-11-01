from flask import Flask

from flasky.config import DevelopmentConfig
from flasky.product.product_view import products_bp
from flasky.auth.views import auth_bp
from flasky.database.postgres import db


def create_app(config_name=None):

    app = Flask(__name__)
    # configure app
    if config_name is not None:
        app.config.from_object(config_name)
    else:
        app.config.from_object(DevelopmentConfig)
        # database setup
        db.connect('my_store', 'Myko', '1987')
        db.create_db_tables()
    # register blueprints
    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)

    return app
