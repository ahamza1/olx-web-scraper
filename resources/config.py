class Config:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class DevConfig(Config):
    FLASK_ENV = 'dev'
    DEBUG = True
    TESTING = True
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"


class ProdConfig(Config):
    FLASK_ENV = 'prod'
    DEBUG = False
    TESTING = False
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"


config_dict = {
    'prod': ProdConfig,
    'dev': DevConfig
}
