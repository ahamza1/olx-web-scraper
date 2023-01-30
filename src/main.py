import threading
import time

from src import config
from src.database import Session
from src.database.db import init_db
from src.database.models import Article, ArticleSearch
from src.services.mail import MailSender
from src.services.scraper import ArticleScraper


def load_articles(article_search):
    scraper = ArticleScraper(config.BASE_URL, config.HEADERS)
    results = scraper.get_articles(article_search.url)

    s = Session()

    existing = s.query(Article) \
        .filter_by(article_search_id=article_search.id, viewed=False).all()

    s.close()

    existing_ids = [e.article_id for e in existing]

    s = Session()
    for r in results:
        if r["id"] not in existing_ids:
            a = Article(
                article_id=r["id"],
                url=r["url"],
                image=r["img"],
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
        .limit(10).all()

    for a in articles:
        a.viewed = True

    ms = MailSender()
    ms.send_articles_notification(article_search.email, articles=articles)

    s.commit()
    s.close()


def start_search():
    print(time.ctime())

    session = Session()
    searches = session.query(ArticleSearch).all()
    session.close()

    for search in searches:
        load_articles(search)

    threading.Timer(1200, start_search).start()


def main():
    init_db()
    start_search()


if __name__ == "__main__":
    main()
