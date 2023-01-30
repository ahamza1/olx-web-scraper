class Config:
    TEMPLATES_FOLDER = 'templates'
    BASE_URL = "https://www.olx.ba"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
