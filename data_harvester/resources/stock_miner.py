import yfinance as yf


class StockMiner:
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = yf.download(self.stock, start=None, end=None)

    def get_daily_stock_data(self):
        return self.stock_data


if __name__ == "__main__":
    sh = StockMiner("TSLA", None, None)
    sh.get_daily_stock_data()
