from urllib import request
from bs4 import BeautifulSoup


class ArticleScraper:
    def __init__(self, base_url, headers) -> None:
        super().__init__()
        self.base_url = base_url
        self.headers = headers

    def get_articles(self, query_path):
        results = []

        while True:
            url = self.base_url + query_path
            page_request = request.Request(url, headers=self.headers)
            page = request.urlopen(page_request)

            html_content = BeautifulSoup(page, 'html.parser')

            articles = html_content.find_all('div', attrs={"class": "artikal"})

            for a in articles:
                article_id = a.get_attribute_list('id')[0]

                if article_id is None:
                    continue

                article_link = a.find_all('a')[0]
                article_url = article_link.get_attribute_list('href')[0]
                article_title = a.find('p', attrs={"class": "na"})

                if article_id:
                    results.append({
                        "id": article_id[4:],
                        "url": article_url,
                        "title": article_title.contents[0]
                    })

            next_page = html_content.find('a', attrs={"rel": "next"})

            if not next_page:
                break

            query_path = next_page.get_attribute_list('href')[0]

        return results
