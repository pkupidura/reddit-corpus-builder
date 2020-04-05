from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from models import Article
from scrapper import FailedScrappingError
from scrapper.article_scrapper_helpers import ArticleScrapperHelpers


class ArticleScrapper(ABC, ArticleScrapperHelpers):
    @staticmethod
    @abstractmethod
    def domain():
        pass

    @abstractmethod
    def scrap_header(self, dom: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def scrap_content(self, dom: BeautifulSoup) -> str:
        pass

    def scrap_article(self, url) -> Article:
        soup = self.get_dom(url)
        try:
            return Article(title=self.scrap_header(soup), body=self.scrap_content(soup), domain=self.domain())
        except Exception as cause:
            raise FailedScrappingError(cause)
