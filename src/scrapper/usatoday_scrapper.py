from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class UsatodayScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "usatoday.com"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(dom)