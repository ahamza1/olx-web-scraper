from urllib import request
from bs4 import BeautifulSoup


class ArticleScraper:
    base_url = "https://www.olx.ba"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    def __init__(self) -> None:
        super().__init__()

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
                article_title = a.find('p', attrs={"class": "na"})

                if article_id:
                    results.append({
                        "id": article_id[4:],
                        "url": f"https://www.olx.ba/artikal/{article_id[4:]}",
                        "title": article_title.contents[0]
                    })

            next_page = html_content.find('a', attrs={"rel": "next"})

            if not next_page:
                break

            query_path = next_page.get_attribute_list('href')[0]

        return results
