from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class FoxnewsArticleScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={'class': 'headline'}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_child_div(dom, attrs={'class': 'article-body'}))

    @staticmethod
    def domain():
        return "foxnews.com"
