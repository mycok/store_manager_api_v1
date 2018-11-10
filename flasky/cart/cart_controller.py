from flasky.product.product_controller import Controller

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
        # check if product is still in stock
        if product_dict['quantity'] == 0:
            return 'Product ' + product_dict['name'] + ' is out of stock'
        elif product_dict['quantity'] < quantity:
            return 'invalid quantity, please check the product stock'

        product_dict['quantity_sold'] += quantity
        product_dict['sales'] += 1
        product_dict['quantity'] -= quantity
        # save the product to cart
        cls.save(product_id, quantity, name=product_dict['name'],
                 category=product_dict['category'],
                 price=product_dict['price'], sales=product_dict['sales'])
        # update the products from the products table
        Controller.update_product(
            name=product_dict['name'], category=product_dict['category'],
            quantity=product_dict['quantity'],
            quantity_sold=product_dict['quantity_sold'],
            price=product_dict['price'], sales=product_dict['sales'],
            product_id=product_id)

    @classmethod
    # save product to the cart table
    def save(cls, product_id, quantity, **kwargs):
        total_amount = kwargs['price'] * quantity

        query = "INSERT INTO cart(product_id, name, category, quantity_sold, amount, sales)\
            VALUES(%s, %s, %s, %s, %s, %s)"

        values = (
            product_id, kwargs['name'], kwargs['category'],
            quantity, total_amount, kwargs['sales'])

        db.insert(query, values)

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
