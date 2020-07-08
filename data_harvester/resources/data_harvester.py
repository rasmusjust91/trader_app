import yfinance as yf

class StockDataHarvester:
    
    def __init__(self, stock):
        self.stock = stock
        # self.ticker = yf.Tickers(self.stock)
        # self.start_date = None
        # self.end_date = None

        # self.stock_info = self.ticker.download(
        #     self.stock,
        #     start='2020-01-01',
        #     end='2020-05-01'
        # )

        self.stock_info = yf.download(
            self.stock,
            start='2020-01-01',
            end='2020-05-01'
        )
    
    def get_stock_data(self):
        return self.stock_info

    # def __fetch_daily_data(self, start_date, end_date):
    #     self.ticker.download(
    #         self.stock,
    #         start=start_date,
    #         end=end_date
    #     )

if __name__ == "__main__":
    sh = StockDataHarvester('TSLA')
    sh.get_stock_data()
