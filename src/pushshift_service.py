import asyncio
import itertools
import math
from dataclasses import dataclass
from datetime import datetime
from time import time as timer
from typing import List

import pushshift_api
from models import Submission, Comment, RawSubmission, SimpleSubmission, SubmissionKind
from submission_filters import filter_by_subreddit, filter_by_subreddit_type, RawSubmissionFilter, filter_by_domains

LOG_ENABLED = True


def log(msg: str):
    if LOG_ENABLED:
        print(msg)


def get_comments(submission: RawSubmission) -> List[Comment]:
    if submission.num_comments == 0:
        return []
    else:
        comment_ids = pushshift_api.get_comment_ids_for_submission(submission.id)
        return pushshift_api.get_comments(comment_ids)


@dataclass
class RawSubmissionWithCommentIds:
    submission: RawSubmission
    comment_ids: List[str]


async def get_submission_comment_ids(submission: RawSubmission) -> RawSubmissionWithCommentIds:
    if submission.num_comments == 0:
        comment_ids = []
    else:
        comment_ids = pushshift_api.get_comment_ids_for_submission(submission.id)

    return RawSubmissionWithCommentIds(submission, comment_ids)


async def get_submissions_with_comment_ids_batch(submissions: List[RawSubmission]) -> List[RawSubmissionWithCommentIds]:
    return await asyncio.gather(*[get_submission_comment_ids(s) for s in submissions])


async def get_submissions_with_comment_ids(submissions: List[RawSubmission]) -> List[RawSubmissionWithCommentIds]:
    result = []

    batch_size = 50

    start = timer()

    for i in range(0, len(submissions), batch_size):
        result.extend(await get_submissions_with_comment_ids_batch(submissions[i:i + batch_size]))

    end = timer()

    log(f'Getting comment ids for {len(submissions)} submissions took {math.ceil(end - start)} seconds.')

    return result


async def get_comments_for_submissions(submissions: List[RawSubmission]) -> List[Submission]:
    st_ts = timer()
    with_comments_ids = await get_submissions_with_comment_ids(submissions)
    en_ts = timer()
    log(f'Getting comment ids took ${en_ts - st_ts}')

    all_comment_ids = list(itertools.chain(*[s.comment_ids for s in with_comments_ids]))

    st_ts = timer()
    all_comments = pushshift_api.get_comments(all_comment_ids)
    en_ts = timer()
    log(f'Getting {len(all_comments)} comments took ${en_ts - st_ts}')

    link_to_comments = {}

    for comment in all_comments:
        link_id = comment.link_id.split("_")[1]
        if link_id not in link_to_comments:
            link_to_comments[link_id] = [comment]
        else:
            link_to_comments[link_id].append(comment)

    return [s.to_submission(link_to_comments.get(s.id, [])) for s in submissions]


async def get_raw_submissions(start: datetime, end: datetime, search_phrase: str) -> List[RawSubmission]:
    st_ts = timer()
    raw_submissions = pushshift_api.search_submissions_in_period(
        int(start.timestamp()),
        int(end.timestamp()),
        search_phrase
    )
    en_ts = timer()
    log(f'Fetching submissions took ${en_ts - st_ts}')

    submission_filters: List[RawSubmissionFilter] = [
        filter_by_domains,
        filter_by_subreddit,
        filter_by_subreddit_type,
        lambda s: not s.is_video,
        lambda s: not s.is_reddit_media_domain,
        lambda s: not s.selftext == "[removed]"
    ]

    def predicate(s) -> bool:
        return all([sf(s) for sf in submission_filters])

    st_ts = timer()
    valid_submissions = [s for s in raw_submissions if predicate(s)]
    en_ts = timer()
    log(f'Filtering took ${en_ts - st_ts}')

    return valid_submissions


async def get_submissions(start: datetime, end: datetime, search_phrase: str) -> List[Submission]:
    valid_submissions = await get_raw_submissions(start, end, search_phrase)

    st_ts = timer()
    with_comments = await get_comments_for_submissions(valid_submissions)
    en_ts = timer()
    log(f'Fetching comments took ${en_ts - st_ts}')

    return with_comments


def scan_submissions_sources(start: datetime, end: datetime, search_phrase: str) -> List[SimpleSubmission]:
    raw_submissions = pushshift_api.search_submissions_in_period(
        int(start.timestamp()),
        int(end.timestamp()),
        search_phrase
    )

    submission_filters: List[RawSubmissionFilter] = [
        filter_by_subreddit_type,
        lambda s: not s.is_video,
        lambda s: not s.is_reddit_media_domain,
        lambda s: not s.selftext == "[removed]"
    ]

    def predicate(s) -> bool:
        return all([sf(s) for sf in submission_filters])

    valid_submissions = [s for s in raw_submissions if predicate(s)]

    def to_source(s: RawSubmission) -> SimpleSubmission:
        return SimpleSubmission(s.subreddit,
                                s.domain,
                                SubmissionKind.POST if s.is_self else SubmissionKind.ARTICLE,
                                s.num_comments,
                                s.selftext)

    return [to_source(s) for s in valid_submissions]
