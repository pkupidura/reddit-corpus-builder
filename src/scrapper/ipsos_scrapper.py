from typing import cast

from bs4 import Tag, BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class IpsosScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        article_container = cast(Tag, dom.find('div', {"id": "block-ipsos-content"}))
        return self.find_child_h1(article_container).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        article_container = cast(Tag, dom.find('div', {"id": "block-ipsos-content"}))
        body_container = cast(Tag, article_container.find("section", attrs={"class": "block-publications-content"}))
        return self.get_paragraphs_text(body_container)

    @staticmethod
    def domain():
        return "ipsos.com"
