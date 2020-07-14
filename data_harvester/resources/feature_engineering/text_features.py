import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim
import string


WORD_VEC_LEN = 300
SHARED_COLUMNS = ["id", "created", "text", "where"]
WORD2VEC_PATH = "resources/models/GoogleNews-vectors-negative300.bin.gz"
PUNCTUATION_TRANSLATOR = str.maketrans("", "", string.punctuation)
STOP_WORDS = set(stopwords.words("english"))
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(
    WORD2VEC_PATH, binary=True
)


def combine_twitter_and_reddit_data(twitter_data, reddit_data):

    twitter_data = twitter_data[
        ["id_str", "created_at", "full_text", "user.screen_name"]
    ]
    twitter_data.columns = SHARED_COLUMNS

    reddit_data = reddit_data[["id", "created", "title", "subreddit"]]
    reddit_data.columns = SHARED_COLUMNS

    combined = pd.concat((twitter_data, reddit_data), ignore_index=True)

    combined["date"] = pd.to_datetime(combined["created"], utc=True).dt.date
    combined["time"] = pd.to_datetime(combined["created"], utc=True).dt.time

    return combined.drop("created", axis=1)


def _text2vec(text, vec_len=WORD_VEC_LEN):

    text = text.lower()
    text = text.translate(PUNCTUATION_TRANSLATOR)
    text = word_tokenize(text)
    filtered_sentence = [w for w in text if not w in STOP_WORDS]
    i = 1
    vector_representation = np.zeros((1, vec_len))

    for word in filtered_sentence:
        try:
            vector_representation = vector_representation + word2vec_model.wv[word]
            i = i + 1
        except KeyError:
            i = i
    vector_representation = np.divide(vector_representation, i)
    return vector_representation[0]


def generate_daily_text_features(data):
    # TODO: Optimize this, its slow!
    data["textvec"] = data["text"].apply(_text2vec)
    text_features = pd.DataFrame(
        data["textvec"].to_list(), columns=[f"textvec_{i}" for i in range(WORD_VEC_LEN)]
    )
    text_features["date"] = data["date"]
    return text_features.groupby("date").agg("mean")


if __name__ == "__main__":
    from resources.utils.io import load_csv_files
    from resources.statics import TWITTER_DATA_PATH, REDDIT_DATA_PATH

    reddit_data = load_csv_files(REDDIT_DATA_PATH)
    twitter_data = load_csv_files(TWITTER_DATA_PATH)

    data = combine_twitter_and_reddit_data(twitter_data, reddit_data)

    features = generate_daily_text_features(data)
    print(features)
