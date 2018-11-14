from tests.fixture import TestFixture
from flasky import config
from flasky import create_app


class TestConfiguration(TestFixture):
    """
    Test class for application configurations
    """

    def test_config(self):
        app = create_app(config.Config)
        self.assertFalse(app.config['DEBUG'])

    def test_development_config(self):
        app = create_app()
        self.assertTrue(app.config['DEBUG'])

    def test_testing_config(self):
        app = create_app(config.TestingConfig)
        self.assertTrue(app.config['TESTING'])

    def test_production_config(self):
        app = create_app(config.ProductionConfig)
        self.assertFalse(app.config['DEBUG'])
