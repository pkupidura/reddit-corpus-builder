from dataclasses import dataclass
from enum import Enum
from typing import List


class SubredditType(Enum):
    PUBLIC = 'public'
    USER = 'user'


@dataclass
class Comment:
    id: str
    body: str
    link_id: str
    parent_id: str


RawComment = Comment


class SubmissionKind(Enum):
    POST = "post"
    ARTICLE = "article"


@dataclass
class SimpleSubmission:
    subreddit: str
    domain: str
    kind: SubmissionKind
    no_of_comments: int
    self_text: str


@dataclass
class Article:
    title: str
    body: str
    domain: str


@dataclass
class Post:
    selftext: str


@dataclass
class RedditMeta:
    id: str
    created_utc: int
    full_link: str
    subreddit: str
    title: str
    is_self: bool
    domain: str
    url: str
    selftext: str


# Article title and body in one file
# id-article-domain-date.txt
# Comments from Reddit in one file
# id-comments-date.txt
@dataclass
class ArticleSubmission:
    content: Article
    comments: List[Comment]
    meta: RedditMeta


# Post title and body in one file
# id-post-subreddit-date.txt
# Comments as above
@dataclass
class SelfSubmission:
    content: Post
    comments: List[Comment]
    meta: RedditMeta


@dataclass
class Submission:
    id: str
    created_utc: int
    full_link: str
    subreddit: str
    title: str
    is_self: bool
    domain: str
    url: str
    selftext: str
    comments: List[Comment]

    def meta(self):
        return RedditMeta(
            self.id,
            self.created_utc,
            self.full_link,
            self.subreddit,
            self.title,
            self.is_self,
            self.domain,
            self.url,
            self.selftext
        )


@dataclass
class RawSubmission:
    id: str
    created_utc: int
    domain: str
    title: str
    is_self: bool
    selftext: str
    subreddit: str
    subreddit_type: str
    num_comments: int
    url: str
    full_link: str
    author: str
    is_video: bool
    is_reddit_media_domain: bool

    def to_submission(self, comments: List[Comment]) -> Submission:
        return Submission(
            id=self.id,
            created_utc=self.created_utc,
            full_link=self.full_link,
            subreddit=self.subreddit,
            title=self.title,
            is_self=self.is_self,
            domain=self.domain,
            url=self.url,
            selftext=self.selftext,
            comments=comments
        )
