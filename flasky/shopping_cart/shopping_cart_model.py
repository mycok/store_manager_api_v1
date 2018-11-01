from flasky.product.product_controller import Controller
from flasky.helper_functions import parse_product_dict


class AddToCart:
    """ class that handles the operations of adding
    or removing products from the shopping cart
    """
    shopping_cart = []

    def __init__(self):
        # add database code here
        pass

    # add products to a sale
    @classmethod
    def insert(cls, name, quantity):
        """
        append products to the shopping cart list

        Arguments:
            name -- name of a product object to add
            quantity -- quantity of a product object to add
        """
        # fetch product to add to shopping cart
        product = controller.fetch_product_by_name(name)
        if product is None:
            return 'product ' + name + ' doesnot exist'
        # check if product is still in stock
        elif product.quantity == 0:
            return 'Product ' + product.name + ' is out of stock'
        elif product.quantity < quantity:
            return 'invalid quantity, please check the product stock'
        cls.update_product_attributes(product, quantity)
        # append the product to shopping cart
        cls.shopping_cart.append(product.product_sale_to_json())

    # adjust sale attributes after sale
    @classmethod
    def update_sale_attributes(cls, sale):
        sale.total_products = len(cls.shopping_cart)
        sale.total_amount = parse_product_dict(cls.shopping_cart)

    # adjust product attributes after sale
    @classmethod
    def update_product_attributes(cls, product, quantity):
        product.sales += 1
        product.quantity -= quantity
        product.quantity_sold = quantity

    # load shopping cart and make a sale
    @classmethod
    def load_shopping_cart(cls):
        return cls.shopping_cart
