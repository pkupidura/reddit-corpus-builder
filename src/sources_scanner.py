from datetime import datetime

import pushshift_service


def scan_sources(start: datetime, end: datetime, phrase: str, output_root: str = ""):
    sources = pushshift_service.scan_submissions_sources(start, end, phrase)
    path = f"{output_root}/{start.date()}.csv"

    with open(path, 'w') as f:
        f.write(f"subreddit,domain,kind,no_of_comments,word_count")
        f.write("\n")

        for s in sources:
            f.write(f"{s.subreddit},{s.domain},{s.kind.value},{s.no_of_comments},{len(s.self_text.split())}")
            f.write("\n")

    print(f"Found {len(sources)} submissions.")
