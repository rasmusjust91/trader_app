import tweepy
import pandas as pd

from data_harvester.resources.twitter_statics import (
    TWITTER_CREDENTIALS,
    TWITTER_DATA_FIELDS,
)


class TweetMiner:

    api = None

    def __init__(self, keys_dict=TWITTER_CREDENTIALS, api=api):

        auth = tweepy.OAuthHandler(keys_dict["api_key"], keys_dict["api_key_secret"])
        auth.set_access_token(
            keys_dict["access_token_key"], keys_dict["access_token_secret"]
        )

        self.api = tweepy.API(auth)

    def search_tweets(self, query, since=None, until=None, return_type="pandas"):

        tweets = tweepy.Cursor(
            self.api.search,
            q=[query],
            lang="en",
            since=since,
            until=until,
            tweet_mode="extended",
        ).items()

        tweets_list = [tweet._json for tweet in tweets]
        print(tweets_list)
        if return_type == "pandas":
            return self.tweets_to_pandas(tweets_list)
        elif return_type == "json":
            return tweets_list

    @staticmethod
    def tweets_to_pandas(json_tweet):
        tweet_df = pd.json_normalize(json_tweet)[TWITTER_DATA_FIELDS].set_index(
            "id_str"
        )

        tweet_df["created_at"] = pd.to_datetime(
            tweet_df["created_at"], format="%a %b %d %H:%M:%S %z %Y"
        )

        return tweet_df


if __name__ == "__main__":
    tm = TweetMiner()
    query = "maersk -RT"
    data_frame = tm.search_tweets(query)

    data_frame.to_csv("no_retweets.csv")
