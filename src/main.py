import threading
import time

from sqlalchemy import column, select
from sqlalchemy.sql import Values

from src import config
from src.database import Session
from src.database.db import init_db
from src.database.models import Article, ArticleSearch
from src.services.mail import MailSender
from src.services.scraper import ArticleScraper


def load_articles(article_search):
    print(f"Loading articles for search: id={ article_search.id }, name={ article_search.title }")

    scraper = ArticleScraper(config.BASE_URL, config.HEADERS)
    results = scraper.get_articles(article_search.url)

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

    s = Session()
    articles = s.query(Article) \
        .filter_by(article_search_id=article_search.id, viewed=False) \
        .limit(config.ARTICLE_NOTIFICATION_LIMIT).all()

    for a in articles:
        a.viewed = True

    ms = MailSender()
    message = ms.send_articles_notification(article_search.email, articles=articles)

    if message is not None:
        print(f"Notification sent for search: "
              f"id={ article_search.id }, name={ article_search.title }, message_id: { message['id'] }")
    else:
        print(f"No new articles for search: "
              f"id={ article_search.id }, name={ article_search.title }")

    s.commit()
    s.close()


def start_search():
    print(f"Search articles started at: time={ time.ctime() }")

    session = Session()
    searches = session.query(ArticleSearch).all()
    session.close()

    for search in searches:
        load_articles(search)

    threading.Timer(config.TIMER_PERIOD, start_search).start()


def main():
    init_db()
    start_search()


if __name__ == "__main__":
    main()
