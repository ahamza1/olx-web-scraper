from scraper import ArticleScraper
from src import config
from src.db import Session, init_db
from src.models import Article, ArticleSearch


def load_articles(article_search):
    scraper = ArticleScraper(config.BASE_URL, config.HEADERS)
    results = scraper.get_articles(article_search.url)

    s = Session()

    existing = s.query(Article)\
        .filter_by(article_search_id=article_search.id, viewed=False).all()

    s.close()

    existing_ids = [e.article_id for e in existing]

    s = Session()
    for r in results:
        if r["id"] not in existing_ids:
            a = Article(
                article_id=r["id"],
                url=r["url"],
                title=r["title"],
                article_search_id=article_search.id,
                viewed=False
            )

            s.add(a)

    s.commit()
    s.close()


def main():
    init_db()

    session = Session()
    searches = session.query(ArticleSearch).all()
    session.close()

    for search in searches:
        load_articles(search)


if __name__ == "__main__":
    main()
