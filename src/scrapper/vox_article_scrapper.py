from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class VoxArticleScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={'class': 'c-page-title'}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.find_child_div(dom, attrs={'class': 'c-entry-content'}).text

    @staticmethod
    def domain():
        return "vox.com"
