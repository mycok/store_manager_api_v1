from flasky.database.postgres import db
import json


class Controller:
    """
    controller class for handling sale order interactions
    """

    def __init__(self):
        pass

    # save a new sale record
    @classmethod
    def add_sale_record(cls, sale):
        query = "INSERT INTO sales (sale_id, attendant, products, total_product, total_amount)\
            VALUES(%s, %s, %s, %s, %s)"
        for index, _ in enumerate(sale.products):
            sale.products[index].pop('created_timestamp')

        sale.products = [json.dumps(product) for product in sale.products]
        values = (sale.sale_id, sale.attendant, sale.products, sale.total_products, sale.total_amount)
        db.insert(query, values)

    # fetch sale record by id
    @classmethod
    def fetch_sale_record(cls, sale_id):
        query = "SELECT * FROM sales WHERE sale_id = '{}'".format(sale_id)
        return db.fetch_one(query)

    # fetch all sale reccords
    @classmethod
    def fetch_all_sale_records(cls):
        query = "SELECT * FROM sales"
        return db.select_query(query)


# create an instance of a sale controller class
controller = Controller()
