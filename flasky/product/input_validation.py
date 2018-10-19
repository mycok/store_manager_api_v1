def is_arg_valid(arg=None):
    return arg is not None and arg != '' and not arg.isspace()


def is_numb_valid(numb=None):
    return numb is not None and numb != 0


def is_product_input_valid(name, category, quantity, price):
    message = None
    if not is_arg_valid(arg=name):
        message = 'please provide a valid product name'
    elif not is_arg_valid(arg=category):
        message = 'please provide a valid product category'
    elif not is_numb_valid(quantity):
        message = 'please provide a valid product quantity'
    elif not is_numb_valid(price):
        message = 'please provide a valid product price'

    if message is not None:
        return message
    return True


def is_sale_input_valid(attendant):
    if not is_arg_valid(arg=attendant):
        return 'please provide a valid attendant name'
    return True
