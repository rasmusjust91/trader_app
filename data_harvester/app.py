from flask import Flask, request
import json
# from data_harvester.resources.data_harvester import StockDataHarvester
from resources.data_harvester import StockDataHarvester

app = Flask(__name__)


@app.route("/fetch_data")
def get_data():
    data = request.get_json(force=True)

    stock = data.get("stock")
    dh = StockDataHarvester(stock)
    stock_data = dh.get_stock_data()  
    response = {
        "data": stock_data.to_json()
    }
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
