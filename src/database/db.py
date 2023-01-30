from src.database import db
from src.database.models import base


def init_db():
    base.metadata.create_all(db)


def cleanup_db():
    base.metadata.drop_all(db)


def recreate_database():
    base.metadata.drop_all(db)
    base.metadata.create_all(db)
