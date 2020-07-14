import tweepy
import pandas as pd

from resources.statics import (
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

        return self.tweets_to_pandas(tweets_list)

    def user_timeline_tweets(self, twitter_user_id, return_type="pandas"):
        tweets = tweepy.Cursor(
            self.api.user_timeline, id=twitter_user_id, tweet_mode="extended"
        ).items()
        tweets_list = [tweet._json for tweet in tweets]

        return self.tweets_to_pandas(tweets_list)

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
    # query = "maersk -RT"
    # query = "from:realDonaldTrump"
    data_frame = tm.user_timeline_tweets("BorisJohnson")

    # data_frame = tm.search_tweets(query)
    # print(data_frame)
    data_frame.to_csv("no_retweets.csv", sep="|")
