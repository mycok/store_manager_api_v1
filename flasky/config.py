import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """This class is used to set the initial configuration
       variables for the app
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'thisshouldkeptsecret')
    DEBUG = False


class DevelopmentConfig(Config):
    """This class is used to set the configuration
       variables necessary for development
     """
    DEBUG = True


class TestingConfig(Config):
    """This class is used to set the configuration
       variables necessary for testing
    """

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """This class is used to set the configuration
       variables necessary for production
    """

    pass
