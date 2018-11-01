class Product(object):
    """
    A class that defines product attributes
    """

    def __init__(self, name, category, quantity, price):
        super(Product, self).__init__()
        self.product_id = 0
        self.name = name
        self.category = category
        self.quantity = quantity
        self.quantity_sold = 0
        self.price = price
        self.sales = 0

    def to_json(self):
        """
        Create a json representation of a product
        """
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'in_stock': self.quantity,
            'total_quantity_sold': self.quantity_sold,
            'price': self.price,
            'sales': self.sales
        }

    def product_sale_to_json(self):
        """
        Create product json representation of a sale order
        """
        return {
            'name': self.name,
            'price': self.price,
            'sales': self.sales,
            'quantity_sold': self.quantity_sold
        }
