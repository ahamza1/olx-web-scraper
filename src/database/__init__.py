from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src import config

base = declarative_base()
db = create_engine(config.SQL_ALCHEMY_URL)
Session = sessionmaker(bind=db)
