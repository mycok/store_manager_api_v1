from flasky.helper_functions import generate_id
from flasky.product.product_model import Product


class Sale:
    """
    class that defines a sale object
    """

    def __init__(self, attendant):
        super(Sale, self).__init__()
        self.sale_id = generate_id()
        self.products = []
        self.attendant = attendant
        self.total_products = 0
        self.total_amount = 0

    def to_json(self):
        """
        convert a sale object into a dictionary
        """
        return {
            'sale_id': self.sale_id,
            'attendant': self.attendant,
            'products': self.products,
            'total_products': self.total_products,
            'total_amount': self.total_amount
        }
