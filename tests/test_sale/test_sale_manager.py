from tests.fixture import FixtureTest
from flasky.sale.manager import sale_manager


class TestSaleManager(FixtureTest):
    """
    Test sale manager initialisation
    """

    def test_sale_manager_init(self):
        self.assertIsInstance(sale_manager.sale_records, dict)

    def test_add_new_sale_increases_sale_records_count(self):
        sale_manager.add_sale_record(self.sale)
        self.assertEqual(len(sale_manager.sale_records), 2)
