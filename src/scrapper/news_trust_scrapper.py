from typing import cast

from bs4 import Tag, BeautifulSoup
from scrapper import FailedScrappingError
from scrapper.article_scrapper import ArticleScrapper


class NewsTrustScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        content = cast(Tag, dom.find("span", attrs={"class": "article-container"}))
        containers = content.find_all("div", attrs={"class": "container"})

        if len(containers) != 2:
            raise FailedScrappingError(f"Unexpected page structure when parsing {dom}")

        return self.find_child_h1(containers[0]).text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        content = cast(Tag, dom.find("span", attrs={"class": "article-container"}))
        containers = content.find_all("div", attrs={"class": "container"})

        if len(containers) != 2:
            raise FailedScrappingError(f"Unexpected page structure when parsing {dom}")

        body_wrapper = self.find_child_div(containers[1], attrs={"class": "body-text"})
        return self.get_paragraphs_text(body_wrapper)

    @staticmethod
    def domain():
        return "news.trust.org"
