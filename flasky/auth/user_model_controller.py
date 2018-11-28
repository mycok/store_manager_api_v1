from flasky.database.postgres import db


class UserController:

    # Controller class for handling and storing user data
    @classmethod
    def create_user(cls, user):
        query = f"""INSERT INTO users (user_id, username, role, email, password)
                    VALUES(
                        '{user.user_id}', '{user.username}',
                        '{user.role}', '{user.email}',
                        '{user.password_hash}')
                """
        db.insert(query)

    @classmethod
    def check_if_user_exists(cls, email):
        query = f"SELECT * FROM users WHERE email = '{email}'"
        return db.fetch_one(query)

    @classmethod
    def fetch_user_by_id(cls, user_id):
        query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
        return db.fetch_one(query)

    @classmethod
    def update_user_role(cls, role, email):
        query = f"UPDATE users SET role = '{role}' WHERE email = '{email}'"
        updated = db.update(query)
        if updated == 1:
            return cls.check_if_user_exists(email)
        return "user role update unsuccessful"

    @classmethod
    def update_user_password(cls, password, email):
        query = f"""UPDATE users SET password = '{password}'
                    WHERE email = '{email}'"""
        updated = db.update(query)
        if updated == 1:
            return cls.check_if_user_exists(email)
        return "password update unsuccessful"

    @classmethod
    def fetch_all_attendants(cls):
        query = f"SELECT * FROM users WHERE role = 'Attendant'"
        attendants = db.fetch_all(query)
        if len(attendants) == 0:
            return "No attendants available"
        return attendants
