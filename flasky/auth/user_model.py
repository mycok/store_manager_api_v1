import datetime
import bcrypt
import jwt

from flasky.helper_functions import generate_id


class User(object):

    # A class that defines a user object

    def __init__(self, username, role, email, password):
        self.user_id = generate_id()
        self.username = username
        self.role = role
        self.email = email
        self.password_hash = User.make_password(password)
        self.created_timestamp = datetime.datetime.now()

    # User password hashing
    @classmethod
    def make_password(cls, raw_password):
        """
        Method used to generate a hashed password

        Arguments:
            raw_password  -- Unhashed password
        """

        return bcrypt.hashpw(raw_password, bcrypt.gensalt())

    @classmethod
    def check_password(cls, password_hash, raw_password):
        """
        Method used to validate password

        Arguments:
            raw_password  --  Unhashed password
        """
        return bcrypt.checkpw(raw_password, password_hash)

    # User authentication
    @classmethod
    def generate_auth_token(cls, user_id):
        """
        Method called to generate a jwt authentication
        token

        Arguments:
            email  -- users email
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=1,
                                                                    seconds=90),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'awesomenessisforever',
                algorithm='HS256'
            )

        except Exception as e:
            return e

    @classmethod
    def decode_auth_token(cls, token):
        """
        Method called to decode a jwt user token
        This method validates the token and returns a user_id

        Arguments:
            token  -- users token
        """
        try:
            payload = jwt.decode(
                token, 'awesomenessisforever', algorithm='HS256')

            ids = payload['sub']
            print(ids)
            return ids

        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'token is invalid, please log in again.'

    def to_json(self):
        # convert a user object into a dictionary

        return {
            "username": self.username,
            "email": self.email,
            "password": self.password_hash,
            "created_at": self.created_timestamp
        }
