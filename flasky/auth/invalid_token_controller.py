from flasky.database.postgres import db


class TokenController:

    # class for handling and storing token data
    @classmethod
    def save_invalid_token(cls, token):
        query = f"INSERT INTO invalidtokens (token) VALUES ('{token.token}')"
        db.insert(query)

    @classmethod
    def check_if_token_exists(cls, token):
        query = f"SELECT * FROM invalidtokens WHERE token = '{token}'"
        return db.fetch_one(query)
