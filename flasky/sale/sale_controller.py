from flasky.helper_functions import search_dict_by_key
from flasky.helper_functions import return_all_dict_values


class Controller:
    """
    controller class for handling sale order interactions
    """

    def __init__(self):
        self.sale_records = {}

    # save a new sale record
    def add_sale_record(self, sale):
            self.sale_records[sale.sale_id] = sale

    # fetch sale record by id
    def fetch_sale_record(self, sale_id):
        value_name = 'sale record'
        return search_dict_by_key(self.sale_records, sale_id, value_name)

    # fetch all sale reccords
    def fetch_all_sale_records(self):
        value_name = 'sales records'
        return return_all_dict_values(self.sale_records, value_name)


# create an instance of a sale controller class
controller = Controller()
