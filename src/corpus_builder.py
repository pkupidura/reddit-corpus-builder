import hashlib
import pathlib
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import List, Dict
from time import time as timer

import pushshift_service
import submission_filters
from models import SelfSubmission, Post, ArticleSubmission, Comment, Submission, Article
from scrapper import article_scrapper_registry, ArticleRequestError, SoupParsingError
from scrapper.article_scrapper_registry import UndefinedDomainScrapperError

LOG_ENABLED = True


def log(msg: str):
    if LOG_ENABLED:
        print(msg)


def string_to_one_line(s: str) -> str:
    return ". ".join([line.strip() for line in s.strip().splitlines()])


def write_comments_to_file(comments: List[Comment], path: str, submission_id: str):
    root_comments = [c for c in comments if submission_id in c.parent_id]

    if len(root_comments) > 0:
        with open(path, 'w') as f:
            for c in root_comments:
                f.write(submission_id)
                f.write("|")
                f.write(string_to_one_line(c.body))
                f.write('\n')


def hash_url(url: str) -> int:
    return int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10 ** 16


def write_article_submission(article: ArticleSubmission, root_path: str):
    article_hash = hash_url(article.meta.url)
    article_path = f'{root_path}/article-{article_hash}-{article.meta.domain.replace(".", "_")}.txt'
    comments_path = f'{root_path}/comments-article-{article_hash}-{article.meta.id}.txt'

    with open(article_path, 'w') as f:
        f.write(article.content.title)
        f.write('\n')
        f.write(article.content.body)

    write_comments_to_file(article.comments, comments_path, article.meta.id)


def write_post_submission(post: SelfSubmission, root_path: str):
    post_path = f'{root_path}/post-{post.meta.id}-{post.meta.domain}.txt'
    comments_path = f'{root_path}/comments-post-{post.meta.id}.txt'

    with open(post_path, 'w') as f:
        f.write(post.content.selftext)

    write_comments_to_file(post.comments, comments_path, post.meta.id)


@dataclass
class ArticleSource:
    domain: str
    url: str


@dataclass
class ArticleScrappingMetrics:
    unknown_domain_counter: int = 0
    failed_request_counter: int = 0
    invalid_html_counter: int = 0
    failed_scrapping_counter: int = 0


def scrap_articles(submissions: List[Submission]) -> Dict[str, Article]:
    sources = [ArticleSource(s.domain, s.url) for s in submissions if not s.is_self]

    unique_sources_map = {}

    for source in sources:
        if source.url not in unique_sources_map:
            unique_sources_map[source.url] = source

    unique_sources = list(unique_sources_map.values())

    results: Dict[str, Article] = {}
    metrics = ArticleScrappingMetrics()

    for us in unique_sources:
        try:
            scrapper = article_scrapper_registry.get_scrapper(us.domain)
            article = scrapper.scrap_article(us.url)
        except UndefinedDomainScrapperError as e:
            metrics.unknown_domain_counter = metrics.unknown_domain_counter + 1
            print(e)
            print(us.url)
        except ArticleRequestError as e:
            metrics.failed_request_counter = metrics.failed_request_counter + 1
            print(e)
        except SoupParsingError as e:
            metrics.invalid_html_counter = metrics.invalid_html_counter + 1
            print(e)
        except Exception as inst:
            metrics.failed_scrapping_counter = metrics.failed_scrapping_counter + 1
            print(f"Failed to parse article from {us.domain}, {us.url}")
            print(inst)
        else:
            results[us.url] = article

    print(f"Articles scraping metrics:\n${metrics}")

    return results


async def scrap_corpus(day: date, phrase: str, output_root: str):
    start = datetime.combine(day, time())
    end = start + timedelta(days=1)

    st_ts = timer()
    submissions = await pushshift_service.get_submissions(start, end, phrase)
    en_ts = timer()
    log(f'Getting submissions with comments took {en_ts - st_ts} seconds')

    st_ts = timer()

    url_to_article = scrap_articles(submissions)

    en_ts = timer()
    log(f'Fetching articles took {en_ts - st_ts} seconds')

    self_submissions = []
    article_submissions = []

    for submission in submissions:
        if submission.is_self and submission.subreddit in submission_filters.ALLOWED_SUBREDDITS:
            self_submissions.append(SelfSubmission(Post(submission.selftext), submission.comments, submission.meta()))
        else:
            article = url_to_article.get(submission.url)

            if article is not None:
                article_submissions.append(ArticleSubmission(article, submission.comments, submission.meta()))

    escaped_phrase = phrase.replace('"', '').replace("'", "").replace(" ", "_")

    base_path = f'{output_root}/{escaped_phrase}'
    pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)

    st_ts = timer()

    for a in article_submissions:
        write_article_submission(a, base_path)

    for p in self_submissions:
        write_post_submission(p, base_path)

    en_ts = timer()
    log(f'Writing to file took {en_ts - st_ts} seconds')
