from flasky.database.postgres import db


class TokenController:

    # class for handling and storing token data
    @classmethod
    def save_invalid_token(cls, token):
        query = "INSERT INTO invalidtoken (token) VALUES\
         (%s)"
        values = (token.token,)
        db.insert(query, values)

    @classmethod
    def check_if_token_exists(cls, token):
        query = "SELECT * FROM invalidtoken WHERE token = '{}'".format(token)
        return db.check(query)
