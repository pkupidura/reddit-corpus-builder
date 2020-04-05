from typing import cast

import requests
from bs4 import BeautifulSoup, Tag, PageElement
from scrapper import ArticleRequestError, SoupParsingError


class ArticleScrapperHelpers:
    def get_dom(self, url: str) -> BeautifulSoup:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
        except Exception as cause:
            raise ArticleRequestError(f"Failed to fetch {url} \n Cause: {cause}")

        if response.status_code != 200:
            raise ArticleRequestError(f"Failed to fetch {url} \n Cause: {response.content}")

        try:
            return BeautifulSoup(response.content, "html.parser")
        except Exception as cause:
            raise SoupParsingError(f"Failed to parse soup for {url} \n Cause: {str(cause)}")

    def find_child(self, elem: Tag, child_name: str, **kwargs) -> PageElement:
        return elem.find(child_name, **kwargs)

    def find_child_div(self, elem: Tag, **kwargs) -> Tag:
        return cast(Tag, self.find_child(elem, 'div', **kwargs))

    def find_child_h1(self, elem: Tag, **kwargs) -> Tag:
        return cast(Tag, self.find_child(elem, 'h1', **kwargs))

    def find_article(self, elem: Tag, **kwargs) -> Tag:
        return cast(Tag, self.find_child(elem, 'article', **kwargs))

    def find_section(self, elem: Tag, **kwargs) -> Tag:
        return cast(Tag, self.find_child(elem, 'section', **kwargs))

    def get_paragraphs_text(self, parent: Tag) -> str:
        paragraphs = parent.find_all('p')
        return ' '.join([p.text for p in paragraphs])
