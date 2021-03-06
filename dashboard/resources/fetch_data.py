import requests
import json
import pandas as pd


def get_data(stock, start_date=None, end_date=None, data_type="pandas"):
    data = json.dumps({"stock": stock, "start_date": start_date, "end_date": end_date})

    response = requests.get("http://0.0.0.0:5000/fetch_data", data=data)
    data = response.json().get("data")

    assert data is not None

    if data_type == "pandas":
        return pd.read_json(data)
    elif data_type == "dict":
        return data
    else:
        raise ValueError("No data_type specified")


if __name__ == "__main__":

    print(pd.read_json(get_data("TSLA")))
