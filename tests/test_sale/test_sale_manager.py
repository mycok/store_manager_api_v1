from tests.fixture import FixtureTest
from flasky.sale.sale_controller import controller


class TestSaleManager(FixtureTest):
    """
    Test sale manager initialisation
    """

    def test_sale_manager_init(self):
        self.assertIsInstance(controller.sale_records, dict)

    def test_add_new_sale_increases_sale_records_count(self):
        controller.add_sale_record(self.sale)
        self.assertEqual(len(controller.sale_records), 3)
