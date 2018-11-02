from flasky.helper_functions import search_dict_by_key
from flasky.helper_functions import return_all_dict_values
from flasky.database.postgres import db


class Controller:
    """
    controller class for handling sale order interactions
    """

    def __init__(self):
        pass

    # save a new sale record
    @classmethod
    def add_sale_record(cls, sale):
        query = "INSERT INTO sales (sale_id, attendant, products, total_products, total_amount)\
            VALUES(%s, %s, %s, %s, %s, %s, %s)"
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
        sales = db.fetch_all(query)
        if not isinstance(sales, list) or len(sales) == 0:
            return "No sales available"
        return sales


# create an instance of a sale controller class
controller = Controller()
