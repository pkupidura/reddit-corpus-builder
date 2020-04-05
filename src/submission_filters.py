from typing import Callable

from models import RawSubmission

RawSubmissionFilter = Callable[[RawSubmission], bool]

ALLOWED_SUBREDDITS = ['AskReddit', 'unpopularopinion', 'teenagers', 'DebateRightists', 'climatechange', 'collapse',
                      'NoStupidQuestions', 'environment', 'ChapoTrapHouse', 'climate', 'Showerthoughts',
                      'climateskeptics', 'changemyview', 'conspiracy', 'The_Donald', 'ClimateOffensive', 'rant',
                      'SandersForPresident', 'TooAfraidToAsk', 'Business_Analyst', 'offmychest', 'vegan',
                      'ClimateActionPlan', 'TrueOffMyChest', 'depression', 'explainlikeimfive', 'AskScienceDiscussion',
                      'Libertarian', 'childfree', 'WayOfTheBern', 'atheism', 'AmItheAsshole', 'CrazyIdeas', 'Advice',
                      'australia', 'ExtinctionRebellion', 'Jokes', 'CasualConversation', 'Christianity', 'Futurology']


def filter_by_domains(submission: RawSubmission) -> bool:
    not_allowed_domains = [
        "youtube.com",
        "twitter.com",
        # Paywall
        "nytimes.com",
        "bloomberg.com"
        "thetimes.co.uk",
        "theatlantic.com"
    ]

    if submission.is_self:
        return True
    else:
        return submission.domain not in not_allowed_domains


def filter_by_subreddit_type(submission: RawSubmission) -> bool:
    allowed_types = [
        "public"
    ]

    return submission.subreddit_type in allowed_types


def filter_by_subreddit(submission: RawSubmission) -> bool:
    banned_subreddits = [
        "TalkativePeople",
        "Microbioma",
        "DebateRightists"
    ]

    return not (submission.subreddit in banned_subreddits)
