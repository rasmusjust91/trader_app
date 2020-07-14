from flask import Flask, request

from resources.data_miner.stock_miner import StockMiner

from resources.utils.io import load_csv_files
from resources.feature_engineering.text_features import (
    combine_twitter_and_reddit_data,
    generate_daily_text_features,
)
import os

from resources.statics import TWITTER_DATA_PATH, REDDIT_DATA_PATH

app = Flask(__name__)


@app.route("/get_daily_textual_features")
def get_daily_textual_features():
    reddit_data = load_csv_files(REDDIT_DATA_PATH)
    twitter_data = load_csv_files(TWITTER_DATA_PATH)

    data = combine_twitter_and_reddit_data(twitter_data, reddit_data)

    features = generate_daily_text_features(data)

    return {"data": features.to_json()}


@app.route("/get_daily_stock_features")
def get_daily_stock_features():

    data = request.get_json(force=True)

    stocks = data.get("stocks")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    sh = StockMiner(stocks, start_date=start_date, end_date=end_date)

    features = sh.get_daily_stock_data()

    return {"data": features.to_json()}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
