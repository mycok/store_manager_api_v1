from flasky.helper_funcs import search_dict_by_key
from flasky.helper_funcs import return_all_dict_values


class ProductManager:
    """
    Manager class for handling product
    interactions and storing product data
    """

    last_id = 0

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        is_existing = self.check_if_product_exists(product.name)
        if is_existing is False:
            self.__class__.last_id += 1
            product.p_id = self.__class__.last_id
            self.products[product.p_id] = product
            return True
        return is_existing

    def check_if_product_exists(self, name):
        products = self.products.values()
        for v in products:
            if v.name == name:
                return 'Product ' + v.name + ' already exists'
        return False

    def fetch_product_by_name(self, name):
        products = self.products.values()
        for v in products:
            if v.name == name:
                return v

    def fetch_product(self, p_id):
        value_name = 'product'
        return search_dict_by_key(self.products, p_id, value_name)

    def fetch_all_products(self):
        value_name = 'products'
        return return_all_dict_values(self.products, value_name)

# create an instance of a product manager class
product_manager = ProductManager()
