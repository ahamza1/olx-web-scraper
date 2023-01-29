import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

base = declarative_base()


class ArticleSearch(base):
    __tablename__ = 'ArticleSearch'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String)
    title = Column(String)
    email = Column(String)
    articles = relationship('Article', backref='ArticleSearch')

    def __repr__(self):
        return "<ArticleSearch(id='{}', url='{}', title={}, email={})>" \
            .format(self.id, self.url, self.title, self.email)


class Article(base):
    __tablename__ = 'Article'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(String)
    url = Column(String)
    title = Column(String)
    viewed = Column(Boolean)
    article_search_id = Column(UUID(as_uuid=True), ForeignKey('ArticleSearch.id'))

    def __repr__(self):
        return "<Article(id='{}', article_id='{}', url='{}', title='{}', viewed={})>" \
            .format(self.id, self.article_id, self.url, self.title, self.viewed)
