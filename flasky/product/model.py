class Product(object):
    """
    A class that defines product attributes
    """

    def __init__(self, name, category, quantity, price):
        super(Product, self).__init__()
        self.p_id = 0
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.sales = 0

    def to_json(self):
        """
        Create a json representation of a product
        """
        return {
            'P_id': self.p_id,
            'name': self.name,
            'category': self.category,
            'quantity': self.quantity,
            'price': self.price
        }
