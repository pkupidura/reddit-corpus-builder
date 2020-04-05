from bs4 import BeautifulSoup
from scrapper.article_scrapper import ArticleScrapper


class DailymailArticleScrapper(ArticleScrapper):
    def scrap_header(self, dom: BeautifulSoup) -> str:
        content = self.find_child_div(dom, attrs={'class': 'article-text'})
        return content.find('h2').text

    def scrap_content(self, dom: BeautifulSoup) -> str:
        content = self.find_child_div(dom, attrs={'class': 'article-text'})

        for video_pane in content.find_all("div", attrs={"class": "mol-video"}):
            video_pane.extract()

        return self.get_paragraphs_text(content)

    @staticmethod
    def domain():
        return "dailymail.co.uk"
