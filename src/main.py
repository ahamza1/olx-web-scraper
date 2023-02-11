import threading
import time

from src import config
from src.database import Session
from src.database.db import init_db
from src.database.models import ArticleSearch
from src.services.articles_service import ArticlesService
from src.services.article_scraper_service import ArticleScraperService


def load_articles(article_search):
    print(f"Loading articles for search: id={ article_search.id }, name={ article_search.title }")

    scraper = ArticleScraperService(config.BASE_URL, config.HEADERS)
    results = scraper.get_articles(article_search.url)

    articles = ArticlesService()
    articles.save_new_articles(article_search, results)
    articles.send_new_articles_notification(article_search)


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
