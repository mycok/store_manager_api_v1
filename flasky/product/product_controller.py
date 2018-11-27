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
            query = f"""INSERT INTO products (
                                            product_id, name, category,
                                            quantity, quantity_sold,
                                            price, sales)
                        VALUES(
                            '{product.product_id}', '{product.name}',
                            '{product.category}', '{product.quantity}',
                            '{product.quantity_sold}', '{product.price}',
                            '{product.sales}')"""

            db.insert(query)
            return
        return f"product {product.name} already exists"

    @classmethod
    def check_if_product_exists(cls, product_name):
        query = f"SELECT * FROM products WHERE name = '{product_name}'"
        return db.fetch_one(query)

    @classmethod
    def fetch_product_by_name(cls, product_name):
        query = f"SELECT * FROM products WHERE name = '{product_name}'"
        product = db.fetch_one(query)
        if product is None:
            return f"product {product_name} does not exist"
        return product

    @classmethod
    def fetch_product_by_id(cls, product_id):
        query = f"SELECT * FROM products WHERE product_id = '{product_id}'"
        product = db.fetch_one(query)
        if product is None:
            return f"product with ID {product_id} doesnot exist"
        return product

    @classmethod
    def fetch_all_products(cls):
        query = "SELECT * FROM products"
        return db.select_query(query)

    @classmethod
    def update_product(cls, **kwargs):

        query = f"""UPDATE products SET name = '{kwargs['name']}',
                                category = '{kwargs['category']}',
                                quantity = '{kwargs['quantity']}',
                                quantity_sold = '{kwargs['quantity_sold']}',
                                price = '{kwargs['price']}',
                                sales = '{kwargs['sales']}'
                                WHERE product_id = '{kwargs['product_id']}'
                """

        updated = db.update(query)
        if updated == 1:
            return cls.fetch_product_by_id(kwargs['product_id'])
        return "product update unsuccessful"

    @classmethod
    def delete_product_by_id(cls, product_id):
        query = f"DELETE FROM products WHERE product_id = '{product_id}'"
        return db.delete(query)
