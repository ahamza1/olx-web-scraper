from sqlalchemy import Values, column, select

from src import config
from src.database import Session
from src.database.models import Article
from src.services.mail_sender_service import MailSenderService


class ArticlesService:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def save_new_articles(article_search, results):
        result_ids = [(r["id"],) for r in results]
        new_articles = Values(column("article_id"), name="new_articles").data(
            result_ids
        )

        query = (
            select(new_articles.c.article_id).outerjoin(
                Article,
                Article.article_id == new_articles.c.article_id
                and Article.article_search_id == article_search.id
                and Article.viewed == False
            ).where(Article.article_id == None)
        )

        s = Session()
        new_articles_ids = set(s.execute(query, {"result_ids": result_ids}, ) or [])
        new_ids = [i[0] for i in new_articles_ids]

        if len(new_ids) > 0:
            for r in results:
                if r["id"] in new_ids:
                    a = Article(
                        article_id=r["id"],
                        url=r["url"],
                        image=r["img"],
                        price=r["price"],
                        title=r["title"],
                        article_search_id=article_search.id,
                        viewed=False
                    )
                    s.add(a)
            s.commit()
        s.close()

    @staticmethod
    def send_new_articles_notification(article_search):
        s = Session()

        articles = s.query(Article) \
            .filter_by(article_search_id=article_search.id, viewed=False) \
            .limit(config.ARTICLE_NOTIFICATION_LIMIT).all()

        for a in articles:
            a.viewed = True

        s.close()

        if len(articles) == 0:
            print(f"No new articles for search: "
                  f"id={article_search.id}, name={article_search.title}")
            return

        ms = MailSenderService()
        message = ms.send_articles_notification(article_search.email, articles=articles)

        if message is not None:
            print(f"Notification sent for search: "
                  f"id={article_search.id}, name={article_search.title}, message_id: {message['id']}")
