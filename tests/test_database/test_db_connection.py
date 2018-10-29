from tests.fixture import TestFixture


# Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=False)


# def tearDownModule(self):
    # clear cached database at the end of running all tests
    # Postgresql.clear_cache()


class TestDB(TestFixture):
    def test_db_connection(self):
        self.assertTrue(self.db.connection)

    def test_insert_user_data(self):
        insert_query = "INSERT INTO users (username, email, password) VALUES\
        (%s, %s, %s)"
        values = ('kibuuka', 'mycovan@gma.com', 'testing')
        self.db.insert(insert_query, values)

        select_query = "SELECT COUNT(*) FROM users"
        rows = self.db.fetch_all(select_query)
        self.assertEqual(len(rows), 1)
