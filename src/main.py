from scraper import ArticleScraper
from src.db import Session, init_db

from src.models import Article

path = "/pretraga?vrsta=samoprodaja&sort_order=desc&kategorija=23&kanton=9&grad%5B0%5D=3969&grad%5B1%5D=5896&do=200000&sacijenom=sacijenom&samosaslikom=samosaslikom&kvadrata_min=55&kvadrata_max=1000&stranica=1"

scraper = ArticleScraper()
results = scraper.get_articles(path)

init_db()

session = Session()
existing = session.query(Article).filter_by(viewed=False).all()
session.close()


session = Session()

ex = [e.article_id for e in existing]

for r in results:
    if r["id"] not in ex:
        a = Article(article_id=r["id"], url=r["url"], title=r["title"], viewed=False)
        session.add(a)

session.commit()
session.close()
