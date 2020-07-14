import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class StockMiner:
    def __init__(self, stocks, start_date=None, end_date=None):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def __get_daily_stock_data(self, remove_nulls=True):

        if isinstance(self.stocks, str):
            self.stock_data = yf.download(
                self.stocks, start=self.start_date, end=self.end_date
            )

        elif isinstance(self.stocks, list):
            stocks_data = []
            for stock in self.stocks:
                stock_data = yf.download(
                    stock, start=self.start_date, end=self.end_date
                )

                stock_data.columns = [stock + "_" + c for c in stock_data.columns]
                stocks_data.append(stock_data)

            self.stock_data = pd.concat(stocks_data, axis=1)

        if remove_nulls:
            self.stock_data = self.stock_data.dropna()

    def __normalize_columns(self, col_list=["Volume"]):

        if not hasattr(self, "stock_data"):
            self.__get_daily_stock_data()

        # TODO: This is horrific coded!!
        cols = []
        for col in self.stock_data.columns:
            for col_l in col_list:
                if col.endswith(col_l):
                    cols.append(col)

        print(self.stock_data.columns)
        print(cols)
        self.stock_data[cols] = MinMaxScaler().fit_transform(self.stock_data[cols])

    def get_daily_stock_data(self, normalize=True):

        if not hasattr(self, "stock_data"):
            self.__get_daily_stock_data()

        if normalize:
            self.__normalize_columns()

        return self.stock_data


if __name__ == "__main__":
    sh = StockMiner(["TSLA", "AAPL"], start_date="2015-01-01")
    print(sh.get_daily_stock_data())
