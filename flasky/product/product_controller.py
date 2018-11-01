from flasky.helper_functions import search_dict_by_key
from flasky.helper_functions import return_all_dict_values
from flasky.helper_functions import generate_id
from flasky.database.postgres import db


class Controller:
    """
    Controller class for handling product
    interactions and storing product data
    """
    @classmethod
    def add_product(cls, product):
        is_existing = cls.check_if_product_exists(product.name)
        if is_existing is None:
            product.product_id = generate_id()
            query = "INSERT INTO products (product_id, name, category, quantity, quantity_sold, price, sales)\
            VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = (product.product_id, product.name, product.category, product.quantity, product.quantity_sold, product.price, product.sales)
            db.insert(query, values)
            return
        return "product {} already exists".format(product.name)

    @classmethod
    def check_if_product_exists(cls, product_name):
        query = "SELECT * FROM products WHERE name = '{}'".format(product_name)
        return db.check(query)

    @classmethod
    def fetch_product_by_name(cls, product_name):
        query = "SELECT * FROM questions WHERE name = '{}'".format(product_name)
        product = db.fetch_one(query)
        if product is None:
            return 'product ' + product_name + ' does not exist'
        return product

    @classmethod
    def fetch_product_by_id(cls, product_id):
        query = "SELECT * FROM products WHERE product_id = '{}'".format(product_id)
        product = db.fetch_one(query)
        if product is None:
            return 'product with ID ' + str(product_id) + ' doesnot exist'
        return product

    @classmethod
    def fetch_all_products(cls):
        query = "SELECT * FROM products"
        products = db.fetch_all(query)
        if not isinstance(products, list) or len(products) == 0:
            return "No products available"
        return products

    @classmethod
    def update_product(cls, name, category, quantity, price, product_id):

        # if name is not None and category is not None and quantity is not None and price is not None:
        query = """UPDATE products SET name = '{}',
         category = '{}', quantity = '{}',
         price = '{}' WHERE product_id = '{}'
         """.format(name, category, quantity, price, product_id)
        return db.update(query)

    @classmethod
    def delete_product_by_id(cls, product_id):
        query = "DELETE FROM products WHERE product_id = '{}'".format(product_id)
        return db.delete(query)
