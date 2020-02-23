# with config, only values in uppercases are actually stored
# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# base config class
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    WTF_CSRF_SECRET_KEY = "a csrf secret key"
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@psqldb:5432/testdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True