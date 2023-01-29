class Config:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    BASE_URL = "https://www.olx.ba"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }


class DevConfig(Config):
    FLASK_ENV = 'dev'
    DEBUG = True
    TESTING = True
    SQL_ALCHEMY_URL = "postgresql://changeme:changeme@localhost:49153/postgres"


class ProdConfig(Config):
    FLASK_ENV = 'prod'
    DEBUG = False
    TESTING = False
    SQL_ALCHEMY_URL = "postgresql://changeme:changeme@localhost:49153/postgres"


config_dict = {
    'prod': ProdConfig,
    'dev': DevConfig
}
