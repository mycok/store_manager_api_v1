class Sale(object):
    """
    class that defines a sale object
    """

    def __init__(self, attendant):
        super(Sale, self).__init__()
        self.sale_id = 0
        self.products = []
        self.attendant = attendant

    def to_json(self):
        """
        convert a sale object into a dictionary
        """
        return {
            'sale_id': self.sale_id,
            'attendant': self.attendant,
            'products': self.products
        }
