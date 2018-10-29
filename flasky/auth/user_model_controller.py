from flasky.database.postgres import DataBase as db


class Controller(object):
    """
    Controller class for handling and storing user data
    """
    def __init__(self):
        self.db = db
        self.db.connect('rides', 'Myko', '1987')
        self.db.create_db_tables()

    def create_user(self, user):
        values = (user.user_id, user.username,
                  user.role, user.email, user.password_hash)
        query = "INSERT INTO users (user_id, username, role, email, password) VALUES\
        ({}, {}, {}, {}, {})".format(*values)
        self.db.insert(query, values)

    def check_if_user_exists(self, email):
        query = "SELECT * FROM users WHERE email = '{}'".format(email)
        return self.db.check(query)

    def fetch_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        return self.db.check(query)

# A user controller instance
controller = Controller()
