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
    HOST = 'ec2-107-22-241-243.compute-1.amazonaws.com'
    DATABASE = 'd3du2vcd5d0031'
    USER = 'yerumrcmmbodcj'
    PASSWORD = 'a1b8aa59b3efb84c23ab7ac94f479c2592dbd1c23658e4a0e01975b0c336e80d'
    PORT = '5432'
