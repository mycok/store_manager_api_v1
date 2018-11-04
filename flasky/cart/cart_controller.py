from flasky.product.product_controller import Controller
from flasky.product.product_model import Product
from flasky.helper_functions import parse_product_dict
from flasky.database.postgres import db


class AddToCart(object):
    """ class that handles the operations of adding
    or removing products from the shopping cart
    """

    def __init__(self):
        # add database code here
        pass

    # add products to a sale
    @classmethod
    def insert(cls, product_id, quantity):
        """
        append products to the shopping cart list

        Arguments:
            name -- name of a product object to add
            quantity -- quantity of a product object to add
        """
        # fetch product to add to shopping cart
        product_dict = Controller.fetch_product_by_id(product_id)
        if not isinstance(product_dict, dict):
            return product_dict
        product = Product(product_dict['name'], product_dict['category'],
                          product_dict['quantity'], product_dict['price'])
        # check if product is still in stock
        if product_dict['quantity'] == 0:
            return 'Product ' + product.name + ' is out of stock'
        elif product_dict['quantity'] < quantity:
            return 'invalid quantity, please check the product stock'
        # cls.update_product_attributes(product, quantity)
        # save the product to cart
        cls.save(product, product_id, quantity)

    @classmethod
    # save product to the cart table
    def save(cls, product, product_id, quantity):
        sales = product.sales + 1
        new_quantity = int(product.quantity) - quantity

        query = "INSERT INTO cart (product_id, name, category, quantity, quantity_sold, price, sales)\
            VALUES(%s, %s, %s, %s, %s, %s, %s)"
        values = (product_id, product.name, product.category, new_quantity, quantity, product.price, sales)
        db.insert(query, values)
        # update the products from the products table
        Controller.update_product(
            name=product.name, category=product.category,
            quantity=new_quantity, price=product.price, product_id=product_id)

    @classmethod
    # load all products from the cart table
    def load_cart(cls):
        query = "SELECT * FROM cart"
        return db.select_query(query)

    # adjust sale attributes after sale
    @classmethod
    def update_sale_attributes(cls, sale, products):
        sale.total_products = len(products)
        sale.total_amount = parse_product_dict(products)
