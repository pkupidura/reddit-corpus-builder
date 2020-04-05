from typing import List, Type

from scrapper.article_scrapper import ArticleScrapper
from scrapper.bbc_article_scrapper import BbcArticleScrapper
from scrapper.breitbart_scrapper import BreitbartScrapper
from scrapper.cbc_scrapper import CbcScrapper
from scrapper.cbsnews_scrapper import CbsnewsScrapper
from scrapper.cnn_article_scrapper import CnnArticleScrapper
from scrapper.common_dreams_scrapper import CommonDreamsScrapper
from scrapper.dailymail_article_scrapper import DailymailArticleScrapper
from scrapper.foxnews_article_scrapper import FoxnewsArticleScrapper
from scrapper.guardian_article_scrapper import GuardianArticleScrapper
from scrapper.ipsos_scrapper import IpsosScrapper
from scrapper.itv_scrapper import ItvScrapper
from scrapper.medium_scrapper import MediumScrapper
from scrapper.msn_article_scrapper import MsnArticleScrapper
from scrapper.national_observer_scrapper import NationalObserverScrapper
from scrapper.news_trust_scrapper import NewsTrustScrapper
from scrapper.phys_scrapper import PhysScrapper
from scrapper.reuters_article_scrapper import ReutersArticleScrapper
from scrapper.the_hill_scrapper import TheHillScrapper
from scrapper.usatoday_scrapper import UsatodayScrapper
from scrapper.venture_beat_scrapper import VentureBeatScrapper
from scrapper.vox_article_scrapper import VoxArticleScrapper
from scrapper.yahoo_scrapper import YahooScrapper


class UndefinedDomainScrapperError(Exception):
    """Scrapper for domain was undefined"""


domain_aliases = {
    'edition.cnn.com': "cnn.com",
    "bbc.co.uk": "bbc.com",
    "eu.usatoday.com": "usatoday.com"
}

scrappers: List[Type[ArticleScrapper]] = [
    CnnArticleScrapper,
    ReutersArticleScrapper,
    FoxnewsArticleScrapper,
    BbcArticleScrapper,
    GuardianArticleScrapper,
    VoxArticleScrapper,
    MsnArticleScrapper,
    DailymailArticleScrapper,
    NewsTrustScrapper,
    CommonDreamsScrapper,
    NationalObserverScrapper,
    BreitbartScrapper,
    IpsosScrapper,
    TheHillScrapper,
    VentureBeatScrapper,
    CbsnewsScrapper,
    CbcScrapper,
    ItvScrapper,
    MediumScrapper,
    PhysScrapper,
    YahooScrapper,
    UsatodayScrapper
]

scrappers_registry = {s.domain(): s for s in scrappers}


def get_scrapper(domain) -> ArticleScrapper:
    aliased_domain = domain_aliases.get(domain)
    resolved_domain = aliased_domain if aliased_domain is not None else domain

    scrapper_class = scrappers_registry.get(resolved_domain)

    if scrapper_class is not None:
        return scrapper_class()
    else:
        raise UndefinedDomainScrapperError(f"No scrapper was defined for domain {domain}")
