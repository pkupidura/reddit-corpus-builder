class ArticleRequestError(Exception):
    """Fetching article HTML failed."""


class SoupParsingError(Exception):
    """Parsing page DOM failed."""


class FailedScrappingError(Exception):
    """Scrapping an article failed."""
