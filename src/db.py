from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.config import config_dict
from src.models import base

config = config_dict["dev"]
db = create_engine(config.SQL_ALCHEMY_URL)

Session = sessionmaker(bind=db)


def init_db():
    base.metadata.create_all(db)


def cleanup_db():
    base.metadata.drop_all(db)


def recreate_database():
    base.metadata.drop_all(db)
    base.metadata.create_all(db)
