from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class PhysScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "phys.org"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(self.find_article(dom, attrs={"class": "news-article"})).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_article(dom, attrs={"class": "news-article"}))
