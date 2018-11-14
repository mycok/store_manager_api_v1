import re


class Validation:

    @classmethod
    def is_valid_length(cls, seq):
            return len(seq) > 2

    @classmethod
    def is_arg_string(cls, arg=None):
        return isinstance(arg, str) and not arg.isdigit()

    @classmethod
    def is_valid_string(cls, arg=None):
        return (arg and cls.is_arg_string(arg) and
                arg != '' and cls.is_valid_length(arg) and not arg.isspace())

    @classmethod
    def is_valid_numb(cls, numb=None):
        return numb and numb != 0 and isinstance(numb, int)

    @classmethod
    def is_valid_currency(cls, currency=None):
        return currency and currency != 0 and isinstance(
            currency, int) or isinstance(
                currency, float)

    @classmethod
    def is_valid_password(cls, password):
        return re.match(r"(?=^.{6,15}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?/&gt;.&lt;,])(?!.*\s).*", password)

    @classmethod
    def is_valid_email(cls, email):
        return re.match(r"\w+@[a-zA-Z_]+?\.[a-zA-Z]", email)

    @classmethod
    def validate_product(cls, **kwargs):
        message = None
        if not cls.is_valid_string(kwargs['name']):
            message = (
                'product name should contain atleast three characters, '
                'and no numbers')
        elif not cls.is_valid_string(kwargs['category']):
            message = (
                'product category should contain atleast three characters, '
                'and no numbers')
        elif not cls.is_valid_numb(kwargs['quantity']):
            message = 'quantity should be a number greater than zero'
        elif not cls.is_valid_currency(kwargs['price']):
            message = 'price should be a number greater than zero'

        if message is not None:
            return message
        return True

    @classmethod
    def validate_sale(cls, attendant):
        if not cls.is_valid_string(attendant):
            return 'please provide a valid attendant name'
        return True

    @classmethod
    def validate_cart_product(cls, product_id, quantity):
        if not cls.is_valid_numb(product_id) or not cls.is_valid_numb(quantity):
            return 'please provide a valid product id or/and quantity'
        return True

    @classmethod
    def validate_user(cls, name, email, password):
        """This function should be called to validate
        provided sign-up form arguments

        Arguments: **kwargs{}
        Returns:
            [bool] -- returns True if all values are valid
        """

        if not cls.is_valid_string(arg=name):
            return 'Please provide the correct name and/or username'
        if not cls.is_valid_email(email):
            return 'invalid email or missing email address'
        if not cls.is_valid_password(password):
            return 'missing password/password should be atleast 4 characters'
        return True

    @classmethod
    def validate_user_login(cls, email, password):
        """
        This function should be called to validate
        user login form arguments

        Arguments:
            username {[str]} -- user's name
            password {[str]} -- user's password
        Returns:
            [bool] -- returns True if all values are valid
        """

        if not cls.is_valid_email(email):
            return 'invalid email or missing email address'
        if not cls.is_valid_password(password):
            return 'missing password/password should be atleast 4 characters'

        return True
