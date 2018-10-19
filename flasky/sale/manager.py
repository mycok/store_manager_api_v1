from flasky.product.manager import product_manager


class SaleManager:
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
        try:
            return self.sale_records[sale_id]
        except KeyError:
            return 'sale record with ID ' + str(sale_id) + ' doesnot exist'

    # fetch all sale reccords
    def fetch_all_sale_records(self):
        if len(self.sale_records) > 0:
            return [v for v in self.sale_records.values()]
        return 'No sale records available'

    # add products to a sale helper method
    def add_products(self, new_sale, name):
        """
        append products to the sale object's products list attribute

        Arguments:
            product {Product} -- An instance of a product object
        """
        product = product_manager.fetch_product_by_name(name)
        new_sale.products.append(product.to_json())


# create an instance of a sale manager class
sale_manager = SaleManager()
