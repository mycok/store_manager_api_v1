def is_arg_valid(arg=None):
    return arg is not None and is_string_arg(arg) and arg != '' and not arg.isspace()


def is_string_arg(arg):
    return isinstance(arg, str) and not arg.isdigit()


def is_numb_valid(numb=None):
    return numb is not None and numb != 0 and isinstance(numb, int)


def is_currency_valid(currency=None):
    return currency is not None and currency != 0 and isinstance(
        currency, int) or isinstance(
            currency, float)


def is_product_input_valid(name=None, category=None,
                           quantity=None, price=None):
    message = None
    if not is_arg_valid(arg=name):
        message = 'please provide a valid product name'
    elif not is_arg_valid(arg=category):
        message = 'please provide a valid product category'
    elif not is_numb_valid(numb=quantity):
        message = 'please provide a valid product quantity'
    elif not is_currency_valid(currency=price):
        message = 'please provide a valid product price'

    if message is not None:
        return message
    return True


def is_sale_input_valid(attendant):
    if not is_arg_valid(arg=attendant):
        return 'please provide a valid attendant name'
    return True


def is_valid_shopping_cart_product(name=None, quantity=None):
    if not is_arg_valid(arg=name):
        return 'please provide a valid product name'
    elif not is_numb_valid(numb=quantity):
        return 'please provide a valid product quantity'
    return True
