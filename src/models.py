import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean

base = declarative_base()


class Article(base):
    __tablename__ = 'Article'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(String)
    url = Column(String)
    title = Column(String)
    viewed = Column(Boolean)

    def __repr__(self):
        return "<Article(id='{}', article_id='{}', viewed={})>" \
            .format(self.id, self.article_id, self.viewed)
