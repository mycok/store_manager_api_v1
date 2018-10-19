class ProductManager:
    """
    Manager class for handling product
    interactions and storing product data
    """

    last_id = 0

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        is_existing = self.check_if_product_exists(product.name)
        if is_existing is False:
            self.__class__.last_id += 1
            product.p_id = self.__class__.last_id
            self.products[product.p_id] = product
            return True
        return is_existing

    def check_if_product_exists(self, name):
        products = self.products.values()
        for v in products:
            if v.name == name:
                return 'Product ' + v.name + ' already exists'
        print(products)
        return False

    def fetch_product_by_name(self, name):
        products = self.products.values()
        for v in products:
            if v.name == name:
                return v

    def fetch_product(self, p_id):
        try:
            return self.products[p_id]
        except KeyError:
            return 'product with ID ' + str(p_id) + ' doesnot exist'

    def fetch_all_products(self):
        if len(self.products) > 0:
            return [v for v in self.products.values()]
        return 'No products available'

# create an instance of a product manager class
product_manager = ProductManager()
