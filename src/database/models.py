import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import base


class ArticleSearch(base):
    __tablename__ = "ArticleSearch"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String)
    title = Column(String)
    email = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.current_timestamp())
    articles = relationship("Article", backref="ArticleSearch")

    def __repr__(self):
        return f"<ArticleSearch(id='{self.id}', url='{self.url}', title={self.title}, " \
               f"email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"


class Article(base):
    __tablename__ = "Article"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_search_id = Column(UUID(as_uuid=True), ForeignKey("ArticleSearch.id"))
    article_id = Column(String)
    url = Column(String)
    image = Column(String)
    title = Column(String)
    price = Column(String)
    viewed = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Article(id='{self.id}', article_id='{self.article_id}', url='{self.url}', title='{self.title}', " \
               f"price={self.price}, viewed={self.viewed}, created_at={self.created_at}, updated_at={self.updated_at})>"
