from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class VentureBeatScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "venturebeat.com"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={"class": "article-title"}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_child_div(dom, attrs={"class": "body-container"}))
