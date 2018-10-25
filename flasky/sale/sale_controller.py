from flasky.helper_funcs import search_dict_by_key
from flasky.helper_funcs import return_all_dict_values


class Controller:
    """
    Manager class for handling sale interactions
    """

    last_id = 0

    def __init__(self):
        self.sale_records = {}

    # save a new sale record
    def add_sale_record(self, sale):
            self.__class__.last_id += 1
            sale.sale_id = self.__class__.last_id
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
