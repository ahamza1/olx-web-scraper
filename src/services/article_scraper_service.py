from urllib import request

from bs4 import BeautifulSoup
from selenium import webdriver
import re


class ArticleScraperService:
    def __init__(self, base_url, headers) -> None:
        super().__init__()
        self.base_url = base_url
        self.headers = headers

    def get_articles(self, query_path):
        results = []

        url = self.base_url + query_path

        driver = webdriver.Chrome()
        driver.get(url)
        page = driver.execute_script('return document.body.innerHTML')
        html_content = BeautifulSoup(''.join(page), 'html.parser')

        pagination = html_content.find("div", class_="olx-pagination-wrapper")
        page_count = len(pagination.find("ul").contents)

        if page_count == 0:
            return

        for i in range(1, page_count):
            url = self.base_url + query_path + f"&page={i}"

            driver = webdriver.Chrome()
            driver.get(url)
            page = driver.execute_script('return document.body.innerHTML')
            html_content = BeautifulSoup(''.join(page), 'html.parser')

            articles = html_content.find("div", class_="articles")

            for a in articles:
                article_link = a.find("a")

                if article_link is None or article_link == -1:
                    continue

                article_url = article_link.get_attribute_list("href")[0]
                article_image = a.find_all("img", class_="listing-image-main")[0]
                article_price = a.find_all("span", class_="smaller")[0]
                article_title = a.find_all("h1", class_="main-heading")[0]

                id = article_url.split("/")[2]
                url = self.base_url + article_url
                image = article_image.get_attribute_list("src")[0]
                price = re.sub('\s+', ' ', article_price.contents[0]).strip()
                title = re.sub('\s+', ' ', article_title.contents[0]).strip()

                results.append({
                    "id": id,
                    "url": url,
                    "img": image,
                    "price": price,
                    "title": title
                })

        return results
