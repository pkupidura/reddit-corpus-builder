from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class CbsnewsScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "cbsnews.com"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={"class": "content__title"}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_section(dom, attrs={"class": "content__body"}))
