from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class CbcScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "cbc.ca"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={"class": "detailHeadline"}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_child_div(dom, attrs={"class": "storyWrapper"}))
