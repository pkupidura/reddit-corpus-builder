from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class ReutersArticleScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        return self.find_child_h1(dom, attrs={'class': 'ArticleHeader_headline'}).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        return self.get_paragraphs_text(self.find_child_div(dom, attrs={'class': 'StandardArticleBody_body'}))

    @staticmethod
    def domain():
        return "reuters.com"
