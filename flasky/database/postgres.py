import psycopg2
import psycopg2.extras
from psycopg2 import Error


class DataBase:
    """
    A class that cretaes a connection to a postgres database.
    connect() method creates a connection to the database.
    create_db_tables() loads database tables.
    drop_db_tables() drops/destroys database tables.
    insert() adds object data into a database table.
    check() searches for availability of a specific object and if found, returns that object.
    update() updates object values for a particular table.
    fetchone() returns a single row table objects.
    fetchmany() returns a list of row table objects.
    fetchall() returns a list of all table objects.
    delete() deletes a particular row data from the table.
    close() terminates a running database connection
    """

    def __init__(self):
        pass

    @classmethod
    def connect(cls, *args):
        try:
            cls.connection = psycopg2.connect(
                dbname=args[0], user=args[1], password=args[2])
            cls.cursor = cls.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            print("...connected....")

        except (Exception, psycopg2.DatabaseError) as error:
            cls.connection.rollback()
            cls.connection.commit()
            print('Failed to connect to the database {}'.format(error))

    @classmethod
    def create_db_tables(cls):
        """creates all the tables for the db"""

        users = """CREATE TABLE IF NOT EXISTS users
                (user_id BIGINT, username VARCHAR(255),
                role VARCHAR(255), email VARCHAR(255) UNIQUE, password VARCHAR(255),
                created_timestamp TIMESTAMP DEFAULT NOW())
                """
        cls.cursor.execute(users)
        cls.connection.commit()

    @classmethod
    def drop_tables(cls):
        users = "DROP TABLE IF EXISTS users CASCADE"
        cls.cursor.execute(users)
        cls.connection.commit()
        print('...dropped...')

    @classmethod
    def insert(cls, insert_query, values):
        try:
            cls.cursor.execute(insert_query, values)
            cls.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            cls.connection.rollback()
            print('Failed to insert data into table {}'.format(error))
        finally:
            cls.close()

    @classmethod
    def check(cls, select_query):
        try:
            cls.cursor.execute(select_query)
            return cls.cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
            print('Failed to select table data {}'.format(error))
        finally:
            cls.close()

    @classmethod
    def update(cls, update_query):
        try:
            cls.cursor.execute(update_query)
            cls.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
            print('Failed to update table data {}'.format(error))

    @classmethod
    def fetch_one(cls, query):
        try:
            cls.cursor.execute(query)
            return cls.cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
            print('Failed to fetch table row data {}'.format(error))

    @classmethod
    def fetch_many(cls, query):
        try:
            cls.cursor.execute(query)
            return cls.cursor.fetch_many()
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
            print('Failed to fetch table row data {}'.format(error))

    @classmethod
    def fetch_all(cls, query):
        try:
            cls.cursor.execute(query)
            return cls.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
            print('Failed to fetch table row data {}'.format(error))

    @classmethod
    def delete(cls, delete_query):
        try:
            cls.cursor.execute(delete_query)
            cls.connection.commit()
            return cls.cursor.rowcount
        except (Exception, psycopg2.DatabaseError) as error:
            if cls.connection:
                cls.connection.rollback()
        print('Failed to delete table row data {}'.format(error))

    @classmethod
    def close(cls):
        if cls.connection:
            cls.cursor.close()
            cls.connection.close()
