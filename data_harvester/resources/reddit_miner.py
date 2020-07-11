import praw
import pandas as pd
from data_harvester.resources.statics import REDDIT_CREDENTIALS, REDDIT_DATA_FIELDS


class RedditMiner:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CREDENTIALS["client_id"],
            client_secret=REDDIT_CREDENTIALS["client_secret"],
            user_agent=REDDIT_CREDENTIALS["user_agent"],
            username=REDDIT_CREDENTIALS["username"],
            password=REDDIT_CREDENTIALS["password"],
        )

    def get_subreddit_data(self, subreddit, limit=10):
        # TODO:
        subreddit = self.reddit.subreddit(subreddit)

        data = {field: [] for field in REDDIT_DATA_FIELDS}

        for submission in subreddit.new(limit=limit):
            for field in REDDIT_DATA_FIELDS:
                data[field].append(getattr(submission, field))

        df = pd.DataFrame(data).set_index("id")
        df["created"] = pd.to_datetime(df["created"], unit="s")
        return df


if __name__ == "__main__":
    rm = RedditMiner()
    subreddit = "worldnews"
    print(rm.get_subreddit_data(subreddit))
