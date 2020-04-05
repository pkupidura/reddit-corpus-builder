from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class TheHillScrapper(ArticleScrapper):
    @staticmethod
    def domain():
        return "thehill.com"

    def scrap_header(self, dom: BeautifulSoup) -> str:
        header_div = self.find_child_div(dom, attrs={"class": ["content-wrapper", "title"]})
        return self.find_child_h1(header_div).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        article = self.find_article(dom, attrs={"class": "node-article"})

        for span in article.find_all('span', attrs={"class": "rollover-people-block"}):
            span.extract()

        return self.get_paragraphs_text(article)
