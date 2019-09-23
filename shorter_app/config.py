import logging


class FixedConfig:
    DEBUG = False
    TESTING = False
    LOG_LOCATION = "./log/shorter.log"
    LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    LOG_LEVEL = logging.DEBUG
    ROOT_DATABASE_URI = "postgresql+psycopg2://postgres:mysecretpassword@localhost"
    DATABASE_NAME = "shorter_dev_db"
    SQLALCHEMY_DATABASE_URI = ROOT_DATABASE_URI + "/" + DATABASE_NAME
    SWAGGER_DOC_PATH = "/documents/"


class DefaultConfig(FixedConfig):
    SERVER_NAME = "localhost:5000"
    ENVIRONMENT_NAME = "development"


class TestConfig(FixedConfig):
    SERVER_NAME = "localhost:5000"
    ENVIRONMENT_NAME = "local_test"
