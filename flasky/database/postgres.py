import psycopg2
import psycopg2.extras


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
    def connect(cls, **kwargs):
        try:
            cls.connection = psycopg2.connect(
                user=kwargs['user'],
                database=kwargs['database'],
                password=kwargs['password']
                )

            cls.cursor = cls.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            print("...connected....")

        except (Exception) as error:
            # cls.connection.rollback()
            # cls.connection.commit()
            print('Failed to connect to the database {}'.format(error))

    @classmethod
    def create_db_tables(cls):
        # create database tables
        create_tables_sql = ('flasky/database/invalid_token_table.sql',
                             'flasky/database/users_table.sql',
                             'flasky/database/products_table.sql',
                             'flasky/database/cart_table.sql',
                             'flasky/database/sales_table.sql')

        for table in create_tables_sql:
            query = open(table, mode='r', encoding='utf-8').read()
            cls.cursor.execute(query)
            cls.connection.commit()

    @classmethod
    def drop_tables(cls):
        # drop/delete all existing tables from the database
        drop_tables_sql = (
            'DROP TABLE IF EXISTS users CASCADE',
            'DROP TABLE IF EXISTS products CASCADE',
            'DROP TABLE IF EXISTS invalidtokens CASCADE',
            'DROP TABLE IF EXISTS cart CASCADE',
            'DROP TABLE IF EXISTS sales CASCADE'
        )

        for table_query in drop_tables_sql:
            cls.cursor.execute(table_query)
            cls.connection.commit()
            print('...dropped...')

    def select_query(self, query):
        items = self.fetch_all(query)
        if not isinstance(items, list) or len(items) == 0:
            return "No items available"
        return items

    def insert(self, insert_query, values):
        try:
            self.cursor.execute(insert_query, values)
            self.connection.commit()
        except (Exception) as error:
            self.connection.rollback()
            print('Failed to insert data into table {}'.format(error))

    def update(self, update_query):
        try:
            self.cursor.execute(update_query)
            self.connection.commit()
            return self.cursor.rowcount
        except (Exception) as error:
            if self.connection:
                self.connection.rollback()
            print('Failed to update table data {}'.format(error))

    def fetch_one(self, fetch_one_query):
        try:
            self.cursor.execute(fetch_one_query)
            return self.cursor.fetchone()
        except (Exception) as error:
            if self.connection:
                self.connection.rollback()
            print('Failed to fetch table row data {}'.format(error))

    def fetch_all(self, fetch_all_query):
        try:
            self.cursor.execute(fetch_all_query)
            return self.cursor.fetchall()
        except (Exception) as error:
            if self.connection:
                self.connection.rollback()
            print('Failed to fetch table row data {}'.format(error))

    def delete(self, delete_query):
        try:
            self.cursor.execute(delete_query)
            self.connection.commit()
            return self.cursor.rowcount
        except (Exception) as error:
            if self.connection:
                self.connection.rollback()
        print('Failed to delete table row data {}'.format(error))

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

# create an instance of the database
db = DataBase()
