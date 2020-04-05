from typing import cast

from bs4 import Tag, BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class BreitbartScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        article_container = cast(Tag, dom.find("article", attrs={"class": "the-article"}))
        return self.find_child_h1(article_container).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        article_container = cast(Tag, dom.find("article", attrs={"class": "the-article"}))
        return self.get_paragraphs_text(self.find_child_div(article_container, attrs={"class": "entry-content"}))

    @staticmethod
    def domain():
        return "breitbart.com"
