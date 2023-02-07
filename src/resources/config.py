class Config:
    MAIL_SCOPES = ["https://mail.google.com/"]
    MAIL_TOKEN_FILE = "token.json"
    MAIL_CREDENTIALS_FILE = "credentials.json"
    MAIL_LOCAL_PORT = 61642

    TEMPLATES_FOLDER = "templates"
    MAIL_TEMPLATE = "mail.html"
    MAIL_SUBJECT = "New Articles Update"

    BASE_URL = "https://www.olx.ba"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"
    TIMER_PERIOD = 1800
    ARTICLE_NOTIFICATION_LIMIT = 10


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQL_ALCHEMY_URL = "postgresql://postgres:postgrespw@localhost:49153/postgres"
    TIMER_PERIOD = 3600
    ARTICLE_NOTIFICATION_LIMIT = 15


config_dict = {
    "dev": DevConfig,
    "prod": ProdConfig,
}
