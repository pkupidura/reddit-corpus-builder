import json
import math
from time import time
from typing import List

import requests
from dacite import from_dict

from models import RawSubmission, Comment

PUSHSHIFT_BASE_URL = 'https://api.pushshift.io/reddit'

COMMENTS_BATCH_SIZE = 1000

LOG_ENABLED = True


def log(msg: str):
    if LOG_ENABLED:
        print(msg)


def get_comment_ids_for_submission(submission_id: str) -> List[str]:
    url = f'{PUSHSHIFT_BASE_URL}/submission/comment_ids/{submission_id}'

    start = time()
    res = requests.get(url)
    end = time()
    log(f'Getting comment ids for {submission_id} took {math.ceil(end - start)} seconds.')

    if res.status_code != 200:
        raise Exception(
            f'Failed to get comment ids for submission {submission_id}: {res.status_code} | {res.content}')
    else:
        return json.loads(res.content)['data']


def get_comments(comment_ids: List[str]) -> List[Comment]:
    result = []

    start = time()

    for i in range(0, len(comment_ids), COMMENTS_BATCH_SIZE):
        result.extend(__get_comments_batch(comment_ids[i:i + COMMENTS_BATCH_SIZE]))

    end = time()

    log(f'Getting {len(comment_ids)} comments took {math.ceil(end - start)} seconds.')

    return result


def __get_comments_batch(comment_ids) -> List[Comment]:
    fields = ['id', 'body', 'link_id', 'parent_id']
    url = f'{PUSHSHIFT_BASE_URL}/comment/search?' \
          f'ids={",".join(comment_ids)}&' \
          f'fields={",".join(fields)}'

    res = requests.get(url)

    if res.status_code != 200:
        log(f'Failed to get comment details: {res.status_code} | {res.content}')
        return []
    else:
        data = json.loads(res.content)['data']
        comments = [from_dict(Comment, row) for row in data]
        return comments


def search_submissions_in_period(period_start, period_end, search_phrase, size=500) -> List[RawSubmission]:
    fields = ['id', 'created_utc', 'domain', 'title', 'is_self', 'selftext', 'url', 'num_comments', 'subreddit',
              'subreddit_type', 'full_link', 'author', 'is_video', 'is_reddit_media_domain']

    base = f'{PUSHSHIFT_BASE_URL}/search/submission'

    url = f'{base}/?' \
          f'q={search_phrase}&' \
          f'after={period_start}&' \
          f'before={period_end}&' \
          f'fields={",".join(fields)}&' \
          f'size={size}'

    start = time()

    res = requests.get(url)

    end = time()

    log(f'Searching submissions took {math.ceil(end - start)}.')

    if res.status_code != 200:
        raise Exception(f'Failed to search submissions: {res.status_code} | {res.content}')
    else:
        data = json.loads(res.content)['data']
        submissions: List[RawSubmission] = []

        for row in data:
            try:
                s = from_dict(RawSubmission, row)
            except Exception as inst:
                print(f'Failed to parse row: {row}')
                print(inst)
            else:
                submissions.append(s)

        if len(submissions) == size:
            new_period_start = submissions[-1].created_utc
            submissions.extend(search_submissions_in_period(new_period_start, period_end, search_phrase, size))

        return submissions
