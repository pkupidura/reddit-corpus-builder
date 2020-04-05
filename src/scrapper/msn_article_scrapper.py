from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class MsnArticleScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        content = self.find_child_div(dom, attrs={'class': 'articlecontent'})
        return self.find_child_h1(content).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        content = self.find_child_div(dom, attrs={'class': 'articlecontent'})
        return self.get_paragraphs_text(content)

    @staticmethod
    def domain():
        return "msn.com"
