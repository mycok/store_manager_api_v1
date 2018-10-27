from flasky.helper_functions import search_dict_by_key
from flasky.helper_functions import return_all_dict_values
from flasky.helper_functions import generate_id


class Controller:
    """
    Controller class for handling product
    interactions and storing product data
    """

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        is_existing = self.check_if_product_exists(product.name)
        if is_existing is False:
            product.product_id = generate_id()
            self.products[product.product_id] = product
            return True
        return is_existing

    def check_if_product_exists(self, name):
        products = self.products.values()
        for product_value in products:
            if product_value.name == name:
                return 'Product ' + product_value.name + ' already exists'
        return False

    def fetch_product_by_name(self, name):
        products = self.products.values()
        for product_value in products:
            if product_value.name == name:
                return product_value

    def fetch_product_by_id(self, product_id):
        value_name = 'product'
        return search_dict_by_key(self.products, product_id, value_name)

    def fetch_all_products(self):
        value_name = 'products'
        return return_all_dict_values(self.products, value_name)

# create an instance of a product controller class
controller = Controller()
